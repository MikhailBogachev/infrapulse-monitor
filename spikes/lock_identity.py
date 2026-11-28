"""Check that the deployed API and an independently opened prefork lock share an inode."""

import errno
import fcntl
import os
import sys
import time
from pathlib import Path
from uuid import UUID

mode = sys.argv[1]
identifier = UUID(sys.argv[2])
path = Path("/locks") / f"{identifier}.execution.lock"


def lock_fixture() -> None:
    with path.open("a") as descriptor:
        stat = os.fstat(descriptor.fileno())
        if mode == "hold":
            fcntl.flock(descriptor, fcntl.LOCK_EX)
            print(stat.st_dev, stat.st_ino, "held", flush=True)
            time.sleep(8)
        elif mode == "busy":
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as error:
                if error.errno in (errno.EAGAIN, errno.EACCES):
                    print(stat.st_dev, stat.st_ino, "held", flush=True)
                    return
                raise
            raise AssertionError("API unexpectedly obtained the active worker lock")
        elif mode == "available":
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            print(stat.st_dev, stat.st_ino, "available", flush=True)
        else:
            raise ValueError("Unknown fixture mode")


if mode == "hold":
    child = os.fork()
    if child == 0:
        lock_fixture()
        sys.exit(0)
    _, status = os.waitpid(child, 0)
    sys.exit(os.waitstatus_to_exitcode(status))

lock_fixture()
