"""TCP listeners and direct socket checks for the isolated Linux firewall fixture."""

import errno
import ipaddress
import socket
import sys
import threading
import time
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


def serve(address: str, port: int, bound: threading.Event | None = None) -> None:
    deadline = time.monotonic() + 5
    with socket.socket(family(address)) as listener:
        if family(address) == socket.AF_INET6:
            listener.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
        while True:
            try:
                listener.bind((address, port))
                break
            except OSError as error:
                if error.errno != errno.EADDRNOTAVAIL or time.monotonic() >= deadline:
                    raise
                time.sleep(0.05)
        listener.listen()
        if bound is not None:
            bound.set()
        while True:
            peer, _ = listener.accept()
            with peer:
                try:
                    peer.sendall(b"ip007")
                except (BrokenPipeError, ConnectionResetError):
                    pass


def handshake(
    address: str, port: int, *, verify_payload: bool = False, timeout: float = 0.5
) -> bool:
    with socket.socket(family(address)) as probe:
        probe.settimeout(timeout)
        try:
            probe.connect((address, port))
        except OSError:
            return False
        if verify_payload:
            assert probe.recv(5, socket.MSG_WAITALL) == b"ip007"
        return True


def ready(addresses: tuple[str, ...], ports: tuple[int, ...]) -> None:
    for port in ports:
        for address in addresses:
            deadline = time.monotonic() + 5
            while not handshake(address, port, verify_payload=True):
                if time.monotonic() >= deadline:
                    raise AssertionError(f"Expected reachable fixture {address}:{port}")
                time.sleep(0.1)
            print(f"Allowed {address}:{port}", flush=True)


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
    rounds = 0
    post_attach = 0
    while not FINISH.exists():
        if ARMED.exists() and not BOUND.exists():
            for address in LOOPBACK[:2]:
                listening = threading.Event()
                threading.Thread(
                    target=serve, args=(address, TARGET_PORT, listening), daemon=True
                ).start()
                assert listening.wait(3), f"Loopback listener did not bind on {address}"
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
    assert rounds > post_attach > 0, (rounds, post_attach)
    print(f"Startup refusal sweeps={rounds}, after attachment={post_attach}", flush=True)
    FINISHED.touch()
    threading.Event().wait()


if __name__ == "__main__":
    mode, *argv = sys.argv[1:]
    if mode == "watch-startup":
        watch_startup()
    elif mode == "wait-startup":
        wait_for(STARTED)
    elif mode == "arm":
        ARMED.touch()
        wait_for(BOUND)
    elif mode == "mark-ready":
        wait_for(BOUND)
        READY.touch()
    elif mode == "finish-startup":
        FINISH.touch()
        wait_for(FINISHED)
    elif mode == "check-after-policy":
        if not READY.exists():
            print("Probe workload refused before policy readiness", flush=True)
            sys.exit(3)
        ready(ALLOWED, (TARGET_PORT,))
        ready((*CONTROL, "::ffff:10.72.0.2"), (CONTROL_PORT,))
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
        ipv4, ipv6, *raw_ports = argv
        addresses = tuple(str(ipaddress.ip_address(address)) for address in (ipv4, ipv6))
        ports = tuple(map(int, raw_ports))
        if mode == "ready":
            ready(addresses, ports)
        elif mode == "serve":
            threads = [
                threading.Thread(target=serve, args=(address, port))
                for address in addresses
                for port in ports
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        else:
            raise ValueError(f"Unknown fixture mode {mode}")
