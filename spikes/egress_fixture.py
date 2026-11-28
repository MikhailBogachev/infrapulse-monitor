"""TCP listeners and direct socket checks for the isolated Linux firewall fixture."""

import errno
import ipaddress
import logging
import os
import selectors
import signal
import socket
import sys
import time
from collections.abc import Callable
from contextlib import ExitStack
from pathlib import Path

TARGET_PORT = 18080
CONTROL_PORT = 18082
ALLOWED = ("10.71.0.2", "fd00:71::2", "::ffff:10.71.0.2")
CONTROL = ("10.72.0.2", "fd00:72::2")
LOOPBACK = ("127.0.0.1", "::1", "::ffff:127.0.0.1")
HOST = ("10.70.0.1", "fd00:70::1")
STARTED = Path("/tmp/startup-active")
ARMED = Path("/tmp/policy-installed")
BOUND = Path("/tmp/listeners-bound")
READY = Path("/tmp/policy-ready")
FINISH = Path("/tmp/startup-finish")
FINISHED = Path("/tmp/startup-finished")
DENIED = (
    *CONTROL,
    "::ffff:10.72.0.2",
    "10.71.0.99",
    "fd00:71::99",
    "10.73.0.2",
    "fd00:73::2",
    *LOOPBACK,
    *HOST,
)


def family(address: str) -> socket.AddressFamily:
    return socket.AF_INET6 if ":" in address else socket.AF_INET


def namespace() -> str:
    path = Path("/proc/self/ns/net")
    return str(path.readlink()) if path.is_symlink() else "unavailable"


def process_start(pid: int, proc: Path = Path("/proc")) -> str | None:
    try:
        stat = (proc / str(pid) / "stat").read_text()
    except FileNotFoundError:
        return None
    # The comm field may contain spaces and closing parentheses.
    return stat.rsplit(") ", 1)[1].split()[19]


def verify_replacement(
    old: str,
    old_pid: int,
    old_start: str,
    new: str,
    pid: int,
    start: str,
    proc: Path = Path("/proc"),
) -> None:
    assert old != new, f"Docker reused the previous container: {old}"
    assert process_start(old_pid, proc) != old_start, (
        f"Previous process still exists: generation={old} pid={old_pid} start={old_start}"
    )
    assert process_start(pid, proc) == start, (
        f"Replacement process changed: generation={new} pid={pid} start={start}"
    )


def policy_ready(generation: str) -> bool:
    try:
        return READY.read_text() == generation
    except FileNotFoundError:
        return False


def bind_listener(stack: ExitStack, address: str, port: int) -> socket.socket:
    deadline = time.monotonic() + 5
    listener = stack.enter_context(socket.socket(family(address)))
    if family(address) == socket.AF_INET6:
        listener.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
    while True:
        try:
            listener.bind((address, port))
            listener.listen()
            return listener
        except OSError as error:
            if error.errno == errno.EADDRNOTAVAIL and time.monotonic() < deadline:
                time.sleep(0.05)
                continue
            logging.error(
                "Bind failed pid=%s netns=%s address=%s:%s", os.getpid(), namespace(), address, port
            )
            for path in (Path("/proc/net/tcp"), Path("/proc/net/tcp6")):
                if path.exists():
                    for row in path.read_text().splitlines()[1:]:
                        local, remote, state = row.split()[1:4]
                        if local.endswith(f":{port:04X}") or remote.endswith(f":{port:04X}"):
                            logging.error(
                                "%s local=%s remote=%s state=%s inode=%s",
                                path,
                                local,
                                remote,
                                state,
                                row.split()[9],
                            )
            raise


def shutdown_requested() -> Callable[[], bool]:
    stopping = False

    def stop(_signum: int, _frame: object) -> None:
        nonlocal stopping
        stopping = True

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    return lambda: stopping


def serve(identity: str, addresses: tuple[str, ...], ports: tuple[int, ...]) -> None:
    stopping = shutdown_requested()
    print(f"Fixture starting identity={identity} pid={os.getpid()} netns={namespace()}", flush=True)
    try:
        with ExitStack() as stack, selectors.DefaultSelector() as selector:
            for port in ports:
                for address in addresses:
                    selector.register(bind_listener(stack, address, port), selectors.EVENT_READ)
            print(
                f"Fixture ready identity={identity} addresses={addresses} ports={ports}", flush=True
            )
            payload = f"{identity}\n".encode()
            while not stopping():
                for key, _ in selector.select(timeout=0.1):
                    assert isinstance(key.fileobj, socket.socket)
                    peer, _ = key.fileobj.accept()
                    with peer:
                        peer.settimeout(0.5)
                        try:
                            peer.sendall(payload)
                        except (BrokenPipeError, ConnectionResetError):
                            pass
    finally:
        print(f"Fixture stopped identity={identity} pid={os.getpid()}", flush=True)


def handshake(
    address: str, port: int, *, identity: str | None = None, timeout: float = 0.5
) -> bool:
    with socket.socket(family(address)) as probe:
        probe.settimeout(timeout)
        try:
            probe.connect((address, port))
        except OSError:
            return False
        if identity is not None:
            expected = f"{identity}\n".encode()
            with probe.makefile("rb") as reader:
                actual = reader.readline(len(expected) + 1)
            assert actual == expected, f"Fixture identity mismatch {address}:{port}: {actual!r}"
        return True


def ready(identity: str, addresses: tuple[str, ...], ports: tuple[int, ...]) -> None:
    for port in ports:
        for address in addresses:
            deadline = time.monotonic() + 5
            while not handshake(address, port, identity=identity):
                if time.monotonic() >= deadline:
                    raise AssertionError(f"Expected reachable fixture {identity} {address}:{port}")
                time.sleep(0.1)
            print(f"Allowed {address}:{port} identity={identity}", flush=True)


def refused(addresses: tuple[str, ...], port: int) -> None:
    for address in addresses:
        assert not handshake(address, port), f"Unexpected established connection {address}:{port}"
        print(f"Denied raw socket {address}:{port}", flush=True)


def wait_for(path: Path) -> None:
    deadline = time.monotonic() + 5
    while not path.exists():
        assert time.monotonic() < deadline, f"Missing startup evidence {path}"
        time.sleep(0.025)


def watch_startup() -> None:
    stopping = shutdown_requested()
    rounds = 0
    post_attach = 0
    print(f"Startup sentinel pid={os.getpid()} netns={namespace()}", flush=True)
    with ExitStack() as listeners:
        while not FINISH.exists() and not stopping():
            if ARMED.exists() and not BOUND.exists():
                for address in LOOPBACK[:2]:
                    bind_listener(listeners, address, TARGET_PORT)
                print("Startup loopback listeners bound", flush=True)
                BOUND.touch()
            attached = READY.exists()
            for address in DENIED:
                assert not handshake(address, TARGET_PORT, timeout=0.04), (
                    f"Forbidden connection during startup/recreation: {address}:{TARGET_PORT}"
                )
            rounds += 1
            post_attach += attached
            STARTED.touch()
            time.sleep(0.025)
    if stopping():
        return
    assert rounds > post_attach > 0, (rounds, post_attach)
    print(f"Startup refusal sweeps={rounds}, after attachment={post_attach}", flush=True)
    FINISHED.touch()
    while not stopping():
        time.sleep(0.1)
    print(f"Startup sentinel stopped pid={os.getpid()} netns={namespace()}", flush=True)


if __name__ == "__main__":
    mode, *argv = sys.argv[1:]
    if mode == "watch-startup":
        watch_startup()
    elif mode == "process-start":
        print(process_start(int(argv[0])) or "")
    elif mode == "verify-replacement":
        old, old_pid, old_start, new, pid, start = argv
        verify_replacement(old, int(old_pid), old_start, new, int(pid), start)
    elif mode == "wait-startup":
        wait_for(STARTED)
        assert not READY.exists(), "Readiness marker survived container creation"
    elif mode == "arm":
        ARMED.touch()
        wait_for(BOUND)
    elif mode == "mark-ready":
        (generation,) = argv
        wait_for(BOUND)
        staged = READY.with_suffix(".staged")
        staged.write_text(generation)
        staged.replace(READY)
        print(f"Policy ready netns={namespace()}", flush=True)
    elif mode == "finish-startup":
        FINISH.touch()
        wait_for(FINISHED)
    elif mode == "check-after-policy":
        run_id, generation = argv
        if not policy_ready(generation):
            print("Probe workload refused before policy readiness", flush=True)
            sys.exit(3)
        ready(f"{run_id}-allowed", ALLOWED, (TARGET_PORT,))
        ready(f"{run_id}-control", (*CONTROL, "::ffff:10.72.0.2"), (CONTROL_PORT,))
        # The fixture sends directly from the worker without the application's URL policy.
        refused(DENIED, TARGET_PORT)
        refused(ALLOWED + HOST, CONTROL_PORT)
    elif mode == "disconnected":
        refused(ALLOWED + CONTROL + HOST, TARGET_PORT)
        refused(CONTROL, CONTROL_PORT)
    elif mode == "sealed":
        refused(LOOPBACK + ALLOWED + CONTROL, TARGET_PORT)
        refused(CONTROL, CONTROL_PORT)
    else:
        identity, ipv4, ipv6, *raw_ports = argv
        addresses = tuple(str(ipaddress.ip_address(address)) for address in (ipv4, ipv6))
        ports = tuple(map(int, raw_ports))
        if mode == "ready":
            ready(identity, addresses, ports)
        elif mode == "serve":
            serve(identity, addresses, ports)
        else:
            raise ValueError(f"Unknown fixture mode {mode}")
