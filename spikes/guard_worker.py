"""AD-014 candidate used only by the disposable Celery experiment."""

import fcntl
import ipaddress
import os
import signal
import ssl
import time
from collections.abc import Callable
from pathlib import Path
from uuid import uuid4

from celery import Task
from celery.exceptions import SoftTimeLimitExceeded
from infrapulse import worker
from sqlalchemy import text
from sqlalchemy.orm import Session
from test_transport import DeadlineStream, OneDial, probe

app = worker.app
QUEUE = "ip007-guard"
app.conf.task_queues += (worker.work_queue(QUEUE),)
GENERATION = str(uuid4())


def incarnation(pid: int) -> str | None:
    try:
        return Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[19]
    except FileNotFoundError:
        return None


def wait_for_file(path: Path) -> None:
    deadline = time.monotonic() + 5
    while not path.exists():
        if time.monotonic() >= deadline:
            raise TimeoutError(path.name)
        time.sleep(0.02)


class GuardStream(DeadlineStream):
    def __init__(
        self, stream: DeadlineStream, before_write: Callable[[], None], written: Callable[[], None]
    ) -> None:
        super().__init__(stream._sock, stream.deadline)
        self.before_write: Callable[[], None] | None = before_write
        self.written = written

    def write(self, buffer: bytes, timeout: float | None = None) -> None:
        if self.before_write is not None:
            self.before_write()
            super().write(buffer, timeout)
            self.written()
            self.before_write = None
        else:
            super().write(buffer, timeout)


class GuardDial(OneDial):
    def __init__(
        self,
        address: str,
        dialing: Callable[[], None],
        before_write: Callable[[], None],
        written: Callable[[], None],
    ) -> None:
        super().__init__(ipaddress.ip_address(address))
        self.dialing = dialing
        self.before_write = before_write
        self.written = written

    def connect_tcp(self, *args: object, **kwargs: object) -> DeadlineStream:
        self.dialing()
        raw = super().connect_tcp(*args, **kwargs)
        before_write, written = self.before_write, self.written

        class TLSStream(DeadlineStream):
            def start_tls(
                self,
                ssl_context: ssl.SSLContext,
                server_hostname: str | None = None,
                timeout: float | None = None,
            ) -> DeadlineStream:
                tls = super().start_tls(ssl_context, server_hostname, timeout)
                return GuardStream(tls, before_write, written)

        return TLSStream(raw._sock, raw.deadline)


def persist(session: Session, monitor: str, job: str, token: int, status: int) -> int | None:
    return session.scalar(
        text(
            "WITH closed AS (UPDATE ip007_guard_run SET owner_pid=NULL "
            "WHERE id=:id AND token=:token AND active_job=:job AND owner_pid IS NOT NULL "
            "RETURNING id) "
            "INSERT INTO ip007_guard_result SELECT id,:job,:token,:status FROM closed "
            "RETURNING status"
        ),
        {"id": monitor, "job": job, "token": token, "status": status},
    )


@app.task(bind=True, name="ip007.guard")
def check(
    task: Task, monitor: str, delivery: str, job: str, mode: str, address: str, port: int
) -> None:
    assert worker.sessions is not None
    root = Path("/locks") / monitor
    identity = {"id": monitor, "job": job, "generation": GENERATION}

    def evidence(label: str, value: str = "") -> None:
        file = root / f"{delivery}.{label}"
        staged = file.with_suffix(f".{label}.{os.getpid()}.tmp")
        staged.write_text(value)
        staged.replace(file)

    evidence(
        f"delivery-{uuid4().hex}",
        f"redelivered={task.request.delivery_info.get('redelivered')} "
        f"delivery_count={(task.request.headers or {}).get('x-delivery-count')}",
    )

    with (root / "execution.lock").open("a") as execution:
        try:
            fcntl.flock(execution, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            evidence("outcome", "busy")
            return

        with (root / "start.lock").open("a") as start, worker.sessions.begin() as session:
            try:
                fcntl.flock(start, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                evidence("outcome", "start-busy")
                return
            state = session.execute(
                text("SELECT * FROM ip007_guard_run WHERE id=:id FOR UPDATE"), identity
            ).one()
            if state.paused:
                evidence("outcome", "paused")
                return
            if state.owner_pid is not None:
                if state.generation == GENERATION:
                    confirmed = incarnation(state.owner_pid) != state.incarnation
                else:
                    proof = root / "stopped-generation"
                    confirmed = proof.exists() and proof.read_text() == state.generation
                if not confirmed:
                    evidence("outcome", "unconfirmed")
                    return
                evidence(
                    "previous-exited",
                    f"{state.generation} {state.owner_pid} {state.incarnation} "
                    f"{time.monotonic_ns()}",
                )
                session.execute(
                    text("INSERT INTO ip007_guard_retired VALUES (:id, :previous)"),
                    {**identity, "previous": state.active_job},
                )
            settled = session.scalar(
                text(
                    "SELECT EXISTS (SELECT 1 FROM ip007_guard_result WHERE id=:id AND job=:job "
                    "UNION ALL SELECT 1 FROM ip007_guard_retired WHERE id=:id AND job=:job)"
                ),
                identity,
            )
            if settled:
                # An abandoned marked attempt stays terminal on broker redelivery.
                session.execute(
                    text("UPDATE ip007_guard_run SET owner_pid=NULL WHERE id=:id"), identity
                )
                session.commit()
                evidence("outcome", "terminal")
                return
            birth = incarnation(os.getpid())
            assert birth is not None
            token = session.scalar(
                text(
                    "UPDATE ip007_guard_run SET token=token+1, active_job=:job, "
                    "owner_pid=:pid, incarnation=:birth, generation=:generation, "
                    "lease=clock_timestamp()+interval '750 milliseconds' "
                    "WHERE id=:id RETURNING token"
                ),
                {**identity, "pid": os.getpid(), "birth": birth},
            )
            db_pid = session.scalar(text("SELECT pg_backend_pid()"))
            session.commit()
            evidence("db-pid", str(db_pid))
            stat = os.fstat(execution.fileno())
            evidence("owner", f"{GENERATION} {os.getpid()} {birth} {stat.st_dev}:{stat.st_ino}")
            evidence("dial-ready")
            if mode == "pause-race":
                wait_for_file(root / f"{delivery}.dial")

            def before_write() -> None:
                evidence("write-ready")
                if mode == "pause-race":
                    wait_for_file(root / f"{delivery}.write")

            def written() -> None:
                fcntl.flock(start, fcntl.LOCK_UN)
                evidence("written")
                if mode == "crash":
                    wait_for_file(root / f"{delivery}.kill")
                    os.kill(os.getpid(), signal.SIGKILL)
                if mode in {"deadline", "replace"}:
                    # Inject a non-cooperative transport phase with the TLS socket still open.
                    try:
                        time.sleep(30)
                    except SoftTimeLimitExceeded:
                        evidence("soft-deadline")
                        time.sleep(30)

            context = ssl.create_default_context(cafile=str(root / "certificate.pem"))
            dial = GuardDial(
                address,
                lambda: evidence("dial-ns", str(time.monotonic_ns())),
                before_write,
                written,
            )
            try:
                with probe(context, dial) as client:
                    status = client.get(f"https://probe.test:{port}/{delivery}").status_code
            except BaseException:
                # After the transport context closes, preserve the marker and retire this child.
                os.kill(os.getpid(), signal.SIGKILL)
                raise
            evidence("client-closed", str(time.monotonic_ns()))

        # The start transaction ended before dial. Settlement takes a fresh connection.
        try:
            with worker.sessions.begin() as session:
                settled_pid = session.scalar(text("SELECT pg_backend_pid()"))
                persisted = persist(session, monitor, job, token, status)
            evidence("settled-db-pid", str(settled_pid))
        except BaseException:
            os.kill(os.getpid(), signal.SIGKILL)
            raise
        assert persisted == 204
    evidence("outcome", "completed")
