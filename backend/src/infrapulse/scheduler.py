import fcntl
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import structlog

from infrapulse.config import Settings, contains_live_process
from infrapulse.logging import configure_logging

STATE = Path("/state")
HEALTH = Path("/tmp/infrapulse-scheduler")
CELERY = [sys.executable, "-m", "celery", "-A", "infrapulse.worker:app"]
log = structlog.get_logger()


def healthy() -> bool:
    return (HEALTH / "control.ready").is_file() and all(
        contains_live_process(HEALTH / name) for name in ("beat", "control")
    )


def stop(children: list[subprocess.Popen[bytes]]) -> None:
    for child in children:
        if child.poll() is None:
            child.terminate()
    deadline = time.monotonic() + 27
    for child in children:
        try:
            child.wait(timeout=max(0, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.wait()


def supervise() -> int:
    configure_logging(Settings.load().log_level)
    stopping = False

    def request_stop(signum: int, frame: object) -> None:
        nonlocal stopping
        stopping = True

    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    HEALTH.mkdir(exist_ok=True)
    (HEALTH / "control.ready").unlink(missing_ok=True)
    with (STATE / "beat.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            log.error("scheduler_child_exited")
            return 1
        children: list[subprocess.Popen[bytes]] = []
        try:
            for name, args in (
                (
                    "beat",
                    ["beat", "--schedule", str(STATE / "celerybeat"), "--pidfile", ""],
                ),
                (
                    "control",
                    ["worker", "-Q", "control", "--concurrency=2", "-n", "control@%h"],
                ),
            ):
                if stopping:
                    break
                # Beat also owns the descriptor if the supervisor is killed first.
                child = subprocess.Popen(
                    CELERY + args,
                    start_new_session=True,
                    pass_fds=(lock.fileno(),) if name == "beat" else (),
                    env={
                        **os.environ,
                        "INFRAPULSE_WORKER_READY_FILE": str(HEALTH / "control.ready"),
                    },
                )
                children.append(child)
                (HEALTH / name).write_text(str(child.pid))
            while not stopping:
                if any(child.poll() is not None for child in children):
                    log.error("scheduler_child_exited")
                    return 1
                time.sleep(0.1)
            log.info("scheduler_shutdown")
            return 0
        finally:
            stop(children)
            for name in ("beat", "control", "control.ready"):
                (HEALTH / name).unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit((0 if healthy() else 1) if sys.argv[1:] == ["health"] else supervise())
