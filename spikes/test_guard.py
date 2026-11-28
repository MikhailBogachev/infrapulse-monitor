"""Process and socket evidence for the AD-014 execution guard candidate."""

import fcntl
import multiprocessing as mp
import os
import signal
import socket
import threading
import time
from contextlib import nullcontext
from multiprocessing.connection import Connection
from pathlib import Path
from uuid import uuid4

import pytest
from infrapulse.config import Settings
from infrapulse.database import make_sync_sessions
from sqlalchemy import text
from sqlalchemy.exc import OperationalError


def child(lock_path: Path, target: tuple[str, int], control: Connection, origin: str) -> None:
    with lock_path.open("a") as guard:
        try:
            fcntl.flock(guard, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            control.send(("busy", origin))
            control.close()
            return

        engine = make_sync_sessions(Settings.load())[0] if origin == "scheduled" else None
        try:
            with (
                socket.create_connection(target, timeout=3) as probe,
                engine.connect() if engine else nullcontext() as connection,
            ):
                probe.sendall(origin.encode() + b"\n")
                control.send(("started", origin))
                if connection is not None:
                    control.send(connection.scalar(text("SELECT pg_backend_pid()")))
                while control.poll(10):
                    command = control.recv()
                    if command == "close":
                        break
                    assert command == "verify-disconnect" and connection is not None
                    try:
                        connection.execute(text("SELECT 1"))
                    except OperationalError:
                        control.send("db-lost")
                    else:
                        raise AssertionError("Fixture connection stayed alive")
                else:
                    raise TimeoutError("Parent did not release the controlled probe")
        finally:
            if engine is not None:
                engine.dispose()
        control.send(("closed", origin))
    control.close()


def test_guard_with_real_processes_and_outbound_connections(tmp_path: Path) -> None:
    monitor = uuid4()
    lock = tmp_path / f"{monitor}.execution.lock"
    records: list[tuple[str, str]] = []
    tracing = threading.Condition()
    active: set[str] = set()
    max_active = 0
    stopped = threading.Event()
    context = mp.get_context("spawn")
    children = []
    channels = []
    engine, sessions = make_sync_sessions(Settings.load())
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        listener.settimeout(0.2)
        target = listener.getsockname()

        def watch(probe: socket.socket) -> None:
            nonlocal max_active
            with probe, probe.makefile("rb") as stream:
                origin = stream.readline().decode().strip()
                with tracing:
                    active.add(origin)
                    max_active = max(max_active, len(active))
                    records.append(("opened", origin))
                    tracing.notify_all()
                stream.read()
                with tracing:
                    active.discard(origin)
                    records.append(("closed", origin))
                    tracing.notify_all()

        def accept() -> None:
            handlers = []
            try:
                while not stopped.is_set():
                    try:
                        peer, _ = listener.accept()
                    except TimeoutError:
                        continue
                    handler = threading.Thread(target=watch, args=(peer,), daemon=True)
                    handler.start()
                    handlers.append(handler)
            finally:
                for handler in handlers:
                    handler.join(timeout=3)

        server = threading.Thread(target=accept, daemon=True)
        server.start()

        def launch(origin: str):
            parent, sender = context.Pipe()
            process = context.Process(target=child, args=(lock, target, sender, origin))
            process.start()
            sender.close()
            children.append(process)
            channels.append(parent)
            assert parent.poll(4), f"{origin} sent no evidence"
            return process, parent, parent.recv()

        def saw(stage: str, origin: str) -> None:
            with tracing:
                assert tracing.wait_for(lambda: (stage, origin) in records, timeout=4)

        try:
            with sessions.begin() as session:
                session.execute(
                    text(
                        "INSERT INTO ip007_guard (id, attempt, lease) "
                        "VALUES (:id, 1, now() + interval '1 second')"
                    ),
                    {"id": monitor},
                )
            original, pipe, status = launch("scheduled")
            assert status == ("started", "scheduled")
            saw("opened", "scheduled")
            duplicate, _, status = launch("duplicate")
            assert status == ("busy", "duplicate")
            duplicate.join(4)
            assert duplicate.exitcode == 0
            manual, _, status = launch("manual-contention")
            assert status == ("busy", "manual-contention")
            manual.join(4)
            assert manual.exitcode == 0

            deadline = time.monotonic() + 4
            while True:
                with sessions() as session:
                    expired = session.scalar(
                        text("SELECT lease < now() FROM ip007_guard WHERE id = :id"),
                        {"id": monitor},
                    )
                if expired:
                    break
                assert time.monotonic() < deadline
                time.sleep(0.05)
            assert pipe.poll(3)
            backend_pid = pipe.recv()
            with sessions.begin() as session:
                assert session.scalar(
                    text("SELECT pg_terminate_backend(:pid)"), {"pid": backend_pid}
                )
            pipe.send("verify-disconnect")
            assert pipe.poll(3) and pipe.recv() == "db-lost"
            contender, _, status = launch("expired-lease")
            assert status == ("busy", "expired-lease")
            contender.join(4)
            assert contender.exitcode == 0
            with tracing:
                assert active == {"scheduled"}

            os.kill(original.pid, signal.SIGKILL)
            original.join(4)
            assert original.exitcode == -signal.SIGKILL
            saw("closed", "scheduled")
            with sessions.begin() as session:
                session.execute(
                    text("UPDATE ip007_guard SET attempt = 2 WHERE id = :id"), {"id": monitor}
                )
                stale = session.execute(
                    text(
                        "UPDATE ip007_guard SET attempt = 3 "
                        "WHERE id = :id AND attempt = 1 RETURNING id"
                    ),
                    {"id": monitor},
                )
                assert stale.scalar() is None

            replacement, replacement_pipe, status = launch("new-execution")
            assert status == ("started", "new-execution")
            saw("opened", "new-execution")
            replacement_pipe.send("close")
            assert replacement_pipe.poll(4) and replacement_pipe.recv() == (
                "closed",
                "new-execution",
            )
            replacement.join(4)
            assert replacement.exitcode == 0
            saw("closed", "new-execution")

            last, last_pipe, status = launch("after-normal-close")
            assert status == ("started", "after-normal-close")
            saw("opened", "after-normal-close")
            last_pipe.send("close")
            last.join(4)
            assert last.exitcode == 0
            saw("closed", "after-normal-close")
            assert max_active == 1
            assert records == [
                ("opened", "scheduled"),
                ("closed", "scheduled"),
                ("opened", "new-execution"),
                ("closed", "new-execution"),
                ("opened", "after-normal-close"),
                ("closed", "after-normal-close"),
            ]
            print(f"Controlled target trace: {records}, max simultaneous={max_active}")
        finally:
            for process in children:
                if process.is_alive():
                    process.kill()
                process.join(4)
                process.close()
            for channel in channels:
                channel.close()
            stopped.set()
            server.join(timeout=4)
            with sessions.begin() as session:
                session.execute(text("DELETE FROM ip007_guard WHERE id = :id"), {"id": monitor})
            engine.dispose()


def outbound_start(
    start_lock: Path, target: tuple[str, int], monitor: str, steps: Connection
) -> None:
    engine, sessions = make_sync_sessions(Settings.load())
    try:
        with start_lock.open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            with sessions() as session:
                paused = session.scalar(
                    text("SELECT paused FROM ip007_guard WHERE id = :id"), {"id": monitor}
                )
            if paused:
                steps.send("skipped")
                return
            steps.send("before-dial")
            assert steps.poll(4) and steps.recv() == "dial"
            with socket.create_connection(target, timeout=3) as probe:
                steps.send("before-write")
                assert steps.poll(4) and steps.recv() == "write"
                probe.sendall(b"GET / HTTP/1.0\r\n\r\n")
            fcntl.flock(lock, fcntl.LOCK_UN)
            steps.send("written")
    finally:
        engine.dispose()
        steps.close()


def test_pause_serializes_with_dial_and_initial_write(tmp_path: Path) -> None:
    start_lock = tmp_path / "fixture.start.lock"
    monitor = str(uuid4())
    engine, sessions = make_sync_sessions(Settings.load())
    context = mp.get_context("spawn")

    with sessions.begin() as session:
        session.execute(
            text(
                "INSERT INTO ip007_guard (id, attempt, lease) "
                "VALUES (:id, 1, now() + interval '5 seconds')"
            ),
            {"id": monitor},
        )

    def pause(timeout: float) -> bool:
        deadline = time.monotonic() + timeout
        with start_lock.open("a") as lock:
            while True:
                try:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        return False
                    time.sleep(0.01)
            with sessions.begin() as session:
                session.execute(
                    text("UPDATE ip007_guard SET paused = true WHERE id = :id"), {"id": monitor}
                )
            return True

    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        listener.settimeout(1)

        def start(contender: Connection) -> mp.Process:
            child = context.Process(
                target=outbound_start, args=(start_lock, listener.getsockname(), monitor, contender)
            )
            child.start()
            return child

        processes = []
        try:
            first, child_end = context.Pipe()
            with first, child_end:
                process = start(child_end)
                processes.append(process)
                assert first.poll(4) and first.recv() == "before-dial"
                assert not pause(0.2)
                first.send("dial")
                assert first.poll(4) and first.recv() == "before-write"
                with listener.accept()[0] as target:
                    target.settimeout(1)
                    assert not pause(0.2)
                    first.send("write")
                    assert first.poll(4) and first.recv() == "written"
                    assert target.recv(64) == b"GET / HTTP/1.0\r\n\r\n"
                process.join(4)
                assert process.exitcode == 0
            assert pause(1)
            second, child_end = context.Pipe()
            with second, child_end:
                process = start(child_end)
                processes.append(process)
                assert second.poll(4) and second.recv() == "skipped"
                process.join(4)
                assert process.exitcode == 0
            listener.settimeout(0.25)
            with pytest.raises(TimeoutError):
                listener.accept()
            print("Pause timed out before dial and write, then committed and blocked a new dial")
        finally:
            for process in processes:
                if process.is_alive():
                    process.kill()
                process.join(4)
                process.close()
            with sessions.begin() as session:
                session.execute(text("DELETE FROM ip007_guard WHERE id = :id"), {"id": monitor})
            engine.dispose()
