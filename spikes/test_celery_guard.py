"""Observe socket lifetimes independently of Celery and PostgreSQL state."""

import fcntl
import ipaddress
import shutil
import socket
import socketserver
import ssl
import threading
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

import pytest
from guard_worker import QUEUE, app, persist
from infrapulse.config import Settings
from infrapulse.database import make_sync_sessions
from sqlalchemy import text
from test_transport import tls_contexts


def until(condition: Callable[[], bool], description: str, timeout: float = 18) -> None:
    deadline = time.monotonic() + timeout
    while not condition():
        if time.monotonic() >= deadline:
            pytest.fail(f"Missing guard evidence: {description}")
        time.sleep(0.025)


@contextmanager
def target(
    root: Path, address: ipaddress.IPv4Address
) -> Iterator[tuple[int, list[tuple[str, int, int]], dict[int, str], set[str]]]:
    context, _ = tls_contexts(root, (address,))
    events: list[tuple[str, int, int]] = []
    requests: dict[int, str] = {}
    release: set[str] = set()

    class Server(socketserver.ThreadingTCPServer):
        daemon_threads = True

        def process_request(self, request: socket.socket, client_address: tuple[str, int]) -> None:
            events.append(("open", client_address[1], time.monotonic_ns()))
            super().process_request(request, client_address)

    class Handler(socketserver.BaseRequestHandler):
        def handle(self) -> None:
            peer = self.client_address[1]
            self.request.settimeout(20)
            try:
                with context.wrap_socket(self.request, server_side=True) as tls:
                    data = b""
                    while not data.endswith(b"\r\n\r\n"):
                        block = tls.recv(4096)
                        if not block:
                            raise AssertionError("Client closed before sending fixture headers")
                        data += block
                    request = data.split(b" ", 2)[1].decode().removeprefix("/")
                    requests[peer] = request
                    tls.settimeout(0.05)
                    sent = False
                    while True:
                        if request in release and not sent:
                            tls.sendall(
                                b"HTTP/1.1 204 No Content\r\n"
                                b"Content-Length: 0\r\nConnection: close\r\n\r\n"
                            )
                            sent = True
                        try:
                            if not tls.recv(4096):
                                break
                        except TimeoutError:
                            pass
            except ConnectionResetError:
                pass
            except ssl.SSLEOFError:
                pass
            finally:
                events.append(("close", peer, time.monotonic_ns()))

    with Server((str(address), 0), Handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield server.server_address[1], events, requests, release
        finally:
            server.shutdown()
            thread.join(timeout=3)


def test_celery_tls_guard() -> None:
    monitor = str(uuid4())
    root = Path("/locks") / monitor
    root.mkdir()
    print(f"Guard monitor {monitor}", flush=True)
    engine, sessions = make_sync_sessions(Settings.load())
    address = ipaddress.IPv4Address(socket.gethostbyname(socket.gethostname()))

    with sessions.begin() as session:
        session.execute(text("INSERT INTO ip007_guard_run(id) VALUES (:id)"), {"id": monitor})

    def scalar(statement: str, **parameters: object) -> object:
        with sessions.begin() as session:
            return session.scalar(text(statement), {"id": monitor, **parameters})

    def disconnect(delivery: str) -> int:
        pid = int(marker(f"{delivery}.db-pid"))
        assert scalar("SELECT pg_terminate_backend(:pid)", pid=pid) is True
        until(
            lambda: scalar("SELECT count(*) FROM pg_stat_activity WHERE pid=:pid", pid=pid) == 0,
            "terminated DB connection",
        )
        return pid

    def marker(name: str, timeout: float = 18) -> str:
        path = root / name
        until(path.exists, name, timeout)
        return path.read_text()

    def verify_exit(previous: str, recovery: str, next_delivery: str) -> None:
        *owner, _ = marker(f"{previous}.owner").split()
        *confirmed, stamp = marker(f"{recovery}.previous-exited").split()
        assert owner == confirmed
        assert int(stamp) < int(marker(f"{next_delivery}.dial-ns"))
        print(f"{previous}: exit verified for {' '.join(confirmed)} at {stamp}", flush=True)

    try:
        with target(root, address) as (port, events, requests, release):

            def submit(delivery: str, *, job: str | None = None, mode: str = "normal") -> None:
                app.send_task(
                    "ip007.guard",
                    args=[monitor, delivery, job or delivery, mode, str(address), port],
                    queue=QUEUE,
                    task_id=f"{monitor}-{job or delivery}",
                    retry=False,
                )

            def expect(delivery: str, status: str) -> None:
                assert marker(f"{delivery}.outcome") == status
                print(f"{delivery}: {status}", flush=True)

            def opened(delivery: str) -> int:
                until(lambda: delivery in requests.values(), f"TLS request {delivery}")
                return next(peer for peer, request in requests.items() if request == delivery)

            def closed(delivery: str) -> None:
                peer = opened(delivery)
                until(
                    lambda: any(event == "close" and p == peer for event, p, _ in events),
                    f"TLS EOF {delivery}",
                )

            def complete(delivery: str) -> None:
                release.add(delivery)
                submit(delivery)
                expect(delivery, "completed")
                closed(delivery)

            def pause(timeout: float) -> bool:
                deadline = time.monotonic() + timeout
                with (root / "start.lock").open("a") as lock:
                    while True:
                        try:
                            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                            break
                        except BlockingIOError:
                            if time.monotonic() >= deadline:
                                return False
                            time.sleep(0.01)
                    assert scalar(
                        "UPDATE ip007_guard_run SET paused=true WHERE id=:id RETURNING paused"
                    )
                    return True

            submit("scheduled", mode="crash")
            opened("scheduled")
            owner = marker("scheduled.owner")
            print(f"initial owner generation/PID/incarnation/device:inode={owner}", flush=True)
            submit("duplicate", job="scheduled")
            expect("duplicate", "busy")
            submit("manual")
            expect("manual", "busy")
            until(
                lambda: (
                    scalar("SELECT lease < clock_timestamp() FROM ip007_guard_run WHERE id=:id")
                    is True
                ),
                "expired lease while TLS is active",
            )
            disconnect("scheduled")
            submit("after-expiry-and-db-loss")
            expect("after-expiry-and-db-loss", "busy")
            assert len(events) == 1
            print(
                "Lease expired and PostgreSQL session disappeared while TLS stayed open", flush=True
            )
            (root / "scheduled.kill").touch()
            closed("scheduled")
            expect("scheduled", "terminal")
            deliveries = [path.read_text() for path in root.glob("scheduled.delivery-*")]
            assert sorted(deliveries) == [
                "redelivered=False delivery_count=None",
                "redelivered=True delivery_count=1",
            ]
            print(f"RabbitMQ deliveries for a single publish: {deliveries}", flush=True)
            complete("after-child-crash")
            verify_exit("scheduled", "scheduled", "after-child-crash")
            assert marker("after-child-crash.owner").split()[1:3] != owner.split()[1:3]
            assert scalar("SELECT token FROM ip007_guard_run WHERE id=:id") == 2
            with sessions.begin() as session:
                assert persist(session, monitor, "scheduled", 1, 204) is None
                assert persist(session, monitor, "after-child-crash", 2, 204) is None
            submit("after-settlement-duplicate", job="after-child-crash")
            expect("after-settlement-duplicate", "terminal")

            submit("db-reconnect")
            opened("db-reconnect")
            lost_pid = disconnect("db-reconnect")
            release.add("db-reconnect")
            expect("db-reconnect", "completed")
            closed("db-reconnect")
            assert int(marker("db-reconnect.settled-db-pid")) != lost_pid
            print("TLS result committed in a new DB session after disconnect", flush=True)

            submit("hard-deadline", mode="deadline")
            hard_peer = opened("hard-deadline")
            marker("hard-deadline.soft-deadline")
            assert not any(stage == "close" and peer == hard_peer for stage, peer, _ in events)
            submit("at-soft-deadline")
            expect("at-soft-deadline", "busy")
            closed("hard-deadline")
            # Celery can acknowledge a hard timeout. Reconcile the marked job explicitly.
            assert scalar("SELECT owner_pid IS NOT NULL FROM ip007_guard_run WHERE id=:id") is True
            for attempt in range(10):
                recovery = f"hard-recovery-{attempt}"
                submit(recovery, job="hard-deadline")
                disposition = marker(f"{recovery}.outcome")
                if disposition == "terminal":
                    print(f"{recovery}: terminal", flush=True)
                    break
                assert disposition in {"unconfirmed", "busy"}
                time.sleep(0.1)
            else:
                pytest.fail("Cannot confirm the hard-deadline child's exit")
            stamps = [stamp for _, peer, stamp in events if peer == hard_peer]
            socket_seconds = (stamps[1] - stamps[0]) / 1e9
            assert 10.5 <= socket_seconds < 15.0, socket_seconds
            complete("after-hard-deadline")
            verify_exit("hard-deadline", recovery, "after-hard-deadline")

            submit("old-generation", mode="replace")
            opened("old-generation")
            generation = marker("old-generation.owner")
            Path("/tmp/guard-replace").write_text(generation)
            closed("old-generation")
            until(Path("/tmp/guard-recreated").exists, "host confirmed recreation", 45)
            submit("untested-generation")
            expect("untested-generation", "unconfirmed")
            proof = Path("/tmp/guard-recreated").read_text()
            assert proof == generation
            (root / "stopped-generation").write_text(proof.split()[0])
            complete("new-generation")
            verify_exit("old-generation", "new-generation", "new-generation")
            new_generation, _, _, new_inode = marker("new-generation.owner").split()
            old_generation, _, _, old_inode = generation.split()
            assert new_generation != old_generation and new_inode == old_inode
            print(f"replaced owner generation/PID/incarnation/inode={generation}", flush=True)
            print(f"replacement generation/device:inode={new_generation} {new_inode}", flush=True)

            before = len(events)
            submit("pause-race", mode="pause-race")
            marker("pause-race.dial-ready")
            assert not pause(0.15)
            assert len(events) == before
            (root / "pause-race.dial").touch()
            marker("pause-race.write-ready")
            assert not pause(0.15)
            assert scalar("SELECT paused FROM ip007_guard_run WHERE id=:id") is False
            assert "pause-race" not in requests.values()
            (root / "pause-race.write").touch()
            opened("pause-race")
            marker("pause-race.written")
            assert pause(1)
            pause_committed = time.monotonic_ns()
            release.add("pause-race")
            expect("pause-race", "completed")
            closed("pause-race")
            assert int(marker("pause-race.client-closed")) >= int(marker("pause-race.dial-ns"))
            submit("after-pause")
            expect("after-pause", "paused")
            assert int(marker("pause-race.dial-ns")) < pause_committed
            assert not (root / "after-pause.dial-ns").exists()
            assert (
                scalar("SELECT count(*) FROM ip007_guard_result WHERE id=:id AND status=204") == 5
            )
            assert scalar("SELECT count(*) FROM ip007_guard_retired WHERE id=:id") == 3

            active: set[int] = set()
            maximum = 0
            base = events[0][2]
            for stage, peer, stamp in sorted(events, key=lambda event: event[2]):
                if stage == "open":
                    active.add(peer)
                    maximum = max(maximum, len(active))
                else:
                    active.remove(peer)
                print(f"TLS +{(stamp - base) / 1e9:.6f}s {stage} {requests.get(peer)} peer={peer}")
            assert len(events) == 16
            assert maximum == 1 and not active
            assert {path.stem for path in root.glob("*.dial-ns")} == set(requests.values())
            print(f"TLS hard-deadline lifetime={socket_seconds:.6f}s, max simultaneous={maximum}")
    finally:
        with sessions.begin() as session:
            session.execute(text("DELETE FROM ip007_guard_run WHERE id=:id"), {"id": monitor})
        engine.dispose()
        shutil.rmtree(root)
