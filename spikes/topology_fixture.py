"""Controlled traffic and prefork workload for the IP-007 Compose verification."""

import fcntl
import ipaddress
import json
import os
import selectors
import socket
import ssl
import sys
import time
from collections.abc import Iterator
from contextlib import ExitStack, contextmanager
from pathlib import Path

import dns.message
import dns.query
import dns.rrset
from egress_fixture import bind_listener, namespace, refused, shutdown_requested
from test_transport import Address, Denied, OneDial, probe, select

ADMISSION = Path("/admission")
POLICY_VERSION = "ip007-compose-v1"
MONITOR = "739ef7c5-0193-4c7d-8da8-de5067e27c6c"
LOCK = Path("/locks") / f"{MONITOR}.execution"
START_LOCK = Path("/locks") / f"{MONITOR}.start"
PORT = 443
DNS = "127.0.0.11"
CONTROL = (("10.213.50.2", "fd42:213:50::2", 5432), ("10.213.50.3", "fd42:213:50::3", 5672))
SERVICES = ("postgres", "rabbitmq")


def log(message: str) -> None:
    print(f"{time.monotonic_ns()} pid={os.getpid()} netns={namespace()} {message}", flush=True)


def refusal(role: str) -> str | None:
    try:
        policy = json.loads((ADMISSION / f"{role}.json").read_text())
    except FileNotFoundError:
        return "missing-policy"
    if (
        policy["version"] != POLICY_VERSION
        or policy["hostname"] != socket.gethostname()
        or policy["netns"] != namespace()
        or policy["expires"] <= time.time()
    ):
        return "stale-policy"
    if role == "checks" and policy["previous"] != "initial":
        try:
            stopped = (ADMISSION / "stopped").read_text().strip()
        except FileNotFoundError:
            return "unconfirmed-generation"
        if stopped != policy["previous"]:
            return "unconfirmed-generation"
    return None


def gate(role: str, command: list[str]) -> None:
    stop = shutdown_requested()
    previous = None
    while not stop():
        reason = refusal(role)
        if reason is None:
            log(f"admitted role={role} generation={socket.gethostname()} version={POLICY_VERSION}")
            os.execvp(command[0], command)
        if reason != previous:
            log(f"waiting role={role} reason={reason}")
            previous = reason
        time.sleep(0.05)


def tls_request(
    address: str, path: str, *, protected: set[Address] | None = None, port: int = PORT
) -> None:
    numeric = ipaddress.ip_address(address)
    if isinstance(numeric, ipaddress.IPv6Address) and numeric.ipv4_mapped:
        numeric = numeric.ipv4_mapped
    dial = OneDial(select([address], (numeric,), protected or set()))
    context = ssl.create_default_context(cafile=str(ADMISSION / "certificate.pem"))
    log(f"dial label={path} peer={address}:{port}")
    with probe(context, dial) as client:
        assert client.get(f"https://probe.test:{port}/{path}").status_code == 204
    assert len(dial.dials) == 1


def hold_connection(label: str) -> None:
    context = ssl.create_default_context(cafile=str(ADMISSION / "certificate.pem"))
    log(f"dial label={label} peer=10.213.51.2:{PORT}")
    with socket.create_connection(("10.213.51.2", PORT), timeout=2) as raw:
        with context.wrap_socket(raw, server_hostname="probe.test") as tls:
            tls.settimeout(22)
            tls.sendall(f"GET /{label} HTTP/1.1\r\nHost: probe.test\r\n\r\n".encode())
            raise AssertionError(f"Expected host to stop old generation, got {tls.recv(1)!r}")


@contextmanager
def locked(path: Path) -> Iterator[str]:
    with path.open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        stat = os.fstat(lock.fileno())
        yield f"{stat.st_dev}:{stat.st_ino}"


def outbound(role: str, label: str) -> bool:
    reason = refusal(role)
    if reason:
        log(f"refused label={label} reason={reason}")
        return False
    if role == "notifications":
        tls_request("10.213.52.2", label)
        return True
    with locked(LOCK) as execution, locked(START_LOCK) as start:
        reason = refusal(role)
        if reason:
            log(f"refused label={label} reason={reason}")
            return False
        log(
            f"locks label={label} execution={execution} start={start} "
            f"generation={socket.gethostname()}"
        )
        if label == "old-generation":
            hold_connection(label)
        else:
            tls_request("10.213.51.2", label)
    log(f"completed label={label}")
    return True


def prefork_check(label: str) -> None:
    assert outbound("checks", label)


if __name__ == "topology_fixture":
    from infrapulse.worker import app

    app.task(name="ip007.topology.check", acks_late=False, soft_time_limit=20, time_limit=25)(
        prefork_check
    )


def dns_check(destination: str, name: str, expected: str | None) -> None:
    query = dns.message.make_query(name, "A")
    for protocol in (dns.query.udp, dns.query.tcp):
        try:
            reply = protocol(query, destination, timeout=0.6)
        except (OSError, TimeoutError, dns.exception.Timeout):
            assert expected is None, (destination, name, protocol)
        else:
            assert expected is not None and str(reply.answer[0][0]) == expected, reply
        log(
            f"DNS protocol={protocol.__name__} resolver={destination} "
            f"name={name} expected={expected}"
        )


def diagnose(role: str) -> None:
    from infrapulse.config import contains_live_process

    ready = Path("/tmp/infrapulse-worker.ready").is_file()
    live = contains_live_process(Path("/tmp/infrapulse-worker.pid"))
    log(
        f"readiness role={role} generation={socket.gethostname()} "
        f"expected_revision={POLICY_VERSION} "
        f"policy={refusal(role) or 'valid'} celery_ready_file={ready} live_pidfile={live}"
    )
    for name, (ipv4, ipv6, port) in zip(SERVICES, CONTROL, strict=True):
        query = dns.message.make_query(f"{name}.", "A")
        for protocol in (dns.query.udp, dns.query.tcp):
            try:
                reply = protocol(query, DNS, timeout=0.6)
                matched = any(str(record) == ipv4 for rrset in reply.answer for record in rrset)
                result = f"rcode={dns.rcode.to_text(reply.rcode())} expected_address={matched}"
            except (OSError, dns.exception.DNSException) as error:
                result = type(error).__name__
            log(f"resolver={DNS} protocol={protocol.__name__} service={name} result={result}")
        for address in (ipv4, ipv6):
            try:
                with socket.create_connection((address, port), timeout=0.6):
                    result = "connected"
            except OSError as error:
                result = f"{type(error).__name__} errno={error.errno}"
            log(f"control service={name} peer={address}:{port} result={result}")


def target() -> None:
    stop = shutdown_requested()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("/tls/certificate.pem", "/tls/key.pem")
    with ExitStack() as stack, selectors.DefaultSelector() as selector:
        for address in ("0.0.0.0", "::"):
            for port in (PORT, 444):
                selector.register(bind_listener(stack, address, port), selectors.EVENT_READ)
        upstream = stack.enter_context(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
        upstream.bind(("0.0.0.0", 53))
        selector.register(upstream, selectors.EVENT_READ)
        dns_tcp = bind_listener(stack, "0.0.0.0", 53)
        selector.register(dns_tcp, selectors.EVENT_READ)
        log(f"target-ready generation={socket.gethostname()}")
        while not stop():
            for key, _ in selector.select(timeout=0.1):
                if key.fileobj == upstream:
                    data, peer = upstream.recvfrom(4096)
                    upstream.sendto(dns_answer(data), peer)
                    continue
                assert isinstance(key.fileobj, socket.socket)
                peer, remote = key.fileobj.accept()
                with peer:
                    peer.settimeout(1)
                    if key.fileobj == dns_tcp:
                        wire = peer.makefile("rb")
                        with wire:
                            size = wire.read(2)
                            if size:
                                reply = dns_answer(wire.read(int.from_bytes(size)))
                                peer.sendall(len(reply).to_bytes(2) + reply)
                    else:
                        accept_tls(context, peer, remote)
    log("target-stopped")


def dns_answer(data: bytes) -> bytes:
    request = dns.message.from_wire(data)
    reply = dns.message.make_response(request)
    name = request.question[0].name.to_text()
    log(f"upstream-query name={name}")
    if name == "probe.test.":
        reply.answer.append(dns.rrset.from_text(name, 0, "IN", "A", "192.0.2.20"))
    else:
        reply.set_rcode(dns.rcode.NXDOMAIN)
    return reply.to_wire()


def accept_tls(
    context: ssl.SSLContext,
    peer: socket.socket,
    remote: tuple[str, int] | tuple[str, int, int, int],
) -> None:
    log(f"accept peer={remote} port={peer.getsockname()[1]}")
    label = ""
    try:
        with context.wrap_socket(peer, server_side=True) as tls, tls.makefile("rb") as request:
            line = request.readline(4096)
            if not line:
                return
            label = line.split()[1].decode().lstrip("/")
            while request.readline(4096) not in (b"", b"\r\n"):
                pass
            log(f"request label={label}")
            if label == "old-generation":
                tls.settimeout(24)
                assert tls.recv(1) == b"", "Old generation did not close its exact socket"
            else:
                tls.sendall(b"HTTP/1.1 204 No Content\r\nConnection: close\r\n\r\n")
    except (ConnectionResetError, ssl.SSLEOFError):
        pass
    finally:
        log(f"close peer={remote} label={label}")


def coverage(role: str) -> None:
    from infrapulse.config import Settings
    from infrapulse.database import make_sync_sessions
    from infrapulse.worker import app
    from sqlalchemy import text

    assert refusal(role) is None
    engine, sessions = make_sync_sessions(Settings.load())
    with sessions() as session:
        assert session.scalar(text("SELECT 1")) == 1
    engine.dispose()
    with app.connection_for_read() as connection:
        connection.connect()
    for ipv4, ipv6, port in CONTROL:
        for address in (ipv4, ipv6):
            with socket.create_connection((address, port), timeout=1):
                log(f"allowed service={address}:{port}")
    mask = 51 if role == "checks" else 52
    primary = (f"10.213.{mask}.2", f"fd42:213:{mask}::2")
    denied = (f"10.213.{mask}.3", f"fd42:213:{mask}::3")
    for address in (*primary, f"::ffff:{primary[0]}"):
        tls_request(address, f"{role}-dualstack")
    with socket.create_connection((f"::ffff:{primary[0]}", PORT), timeout=1):
        log(f"Allowed raw mapped socket peer=::ffff:{primary[0]}:{PORT}")
    refused(denied + (f"::ffff:{denied[0]}",), PORT)
    refused(primary + denied, 444)
    if role == "checks":
        refused(("10.213.51.1", "fd42:213:51::1"), 18080)
        refused(("10.213.51.1", "fd42:213:51::1"), 18081)
    for name, (ipv4, _, _) in zip(SERVICES, CONTROL, strict=True):
        dns_check(DNS, f"{name}.", ipv4)
    # Use the embedded resolver's configured, contained upstream. Direct calls
    # to the same test DNS server from the workload are checked over TCP below.
    dns_check(DNS, "probe.test.", "192.0.2.20")
    dns_check(denied[0], "probe.test.", None)
    dns_check(primary[0], "probe.test.", None)
    refused((DNS,), 54)
    with ExitStack() as stack:
        for address in ("127.0.0.1", "::1"):
            listener = bind_listener(stack, address, 0)
            refused((address,), listener.getsockname()[1])
    # Exact control services remain reachable even with the conflicting target
    # allowance. The same HTTPX call path rejects the protected address before a dial.
    for ipv4, ipv6, service_port in CONTROL:
        for address in (ipv4, ipv6, f"::ffff:{ipv4}"):
            with expect_denied(address):
                tls_request(
                    address,
                    "prohibited-http-target",
                    protected={ipaddress.ip_address(ipv4), ipaddress.ip_address(ipv6)},
                    port=service_port,
                )


@contextmanager
def expect_denied(address: str) -> Iterator[None]:
    try:
        yield
    except Denied:
        log(f"HTTP target refused before dial address={address}")
    else:
        raise AssertionError(f"Unexpected HTTP target approval {address}")


if __name__ == "__main__":
    mode, *args = sys.argv[1:]
    if mode == "target":
        target()
    elif mode == "gate":
        gate(args[0], args[1:])
    elif mode == "attempt":
        sys.exit(0 if outbound(*args) else 3)
    elif mode == "coverage":
        coverage(*args)
    elif mode == "diagnose":
        diagnose(*args)
    elif mode == "held":
        segment = 51 if args[0] == "checks" else 52
        refused((f"10.213.{segment}.2", f"fd42:213:{segment}::2"), PORT)
        refused(CONTROL[0][:2], CONTROL[0][2])
    elif mode == "send":
        from infrapulse.worker import app

        app.send_task("ip007.topology.check", args=args, queue="check")
    else:
        raise ValueError(mode)
