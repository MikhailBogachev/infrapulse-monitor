"""Candidate HTTPX transport against isolated local TCP and TLS endpoints."""

import ipaddress
import socket
import socketserver
import ssl
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import dns.flags
import dns.message
import dns.query
import dns.rdatatype
import dns.rrset
import httpcore
import httpx
import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID
from httpcore._backends.sync import SyncStream

type Address = ipaddress.IPv4Address | ipaddress.IPv6Address
PRIVATE = tuple(
    map(ipaddress.ip_network, ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "fc00::/7"])
)


class Denied(ValueError):
    pass


def select(answers: list[str], permitted: tuple[Address, ...], protected: set[Address]) -> Address:
    addresses: list[Address] = []
    for answer in answers:
        address = ipaddress.ip_address(answer)
        if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped:
            address = address.ipv4_mapped
        if (
            address in protected
            or address.is_loopback
            or address.is_link_local
            or address.is_unspecified
            or address.is_multicast
            or address.is_reserved
        ):
            raise Denied("Always denied")
        if not address.is_global and not (
            any(address in network for network in PRIVATE) and address in permitted
        ):
            raise Denied("No internal allowlist match")
        addresses.append(address)
    if not addresses:
        raise Denied("No complete answer")
    return addresses[0]


class DeadlineStream(SyncStream):
    def __init__(self, sock: socket.socket, deadline: float) -> None:
        super().__init__(sock)
        self.deadline = deadline

    def remaining(self, timeout: float | None) -> float:
        budget = self.deadline - time.monotonic()
        if budget <= 0:
            raise httpcore.ReadTimeout("Fixture deadline exhausted")
        return min(timeout, budget) if timeout is not None else budget

    def read(self, max_bytes: int, timeout: float | None = None) -> bytes:
        return super().read(max_bytes, self.remaining(timeout))

    def write(self, buffer: bytes, timeout: float | None = None) -> None:
        super().write(buffer, self.remaining(timeout))

    def start_tls(
        self,
        ssl_context: ssl.SSLContext,
        server_hostname: str | None = None,
        timeout: float | None = None,
    ) -> "DeadlineStream":
        self._sock.settimeout(self.remaining(timeout))
        try:
            tls = ssl_context.wrap_socket(self._sock, server_hostname=server_hostname)
        except (OSError, ValueError) as error:
            self.close()
            raise httpcore.ConnectError("Fixture TLS handshake failed") from error
        return DeadlineStream(tls, self.deadline)


class OneDial(httpcore.SyncBackend):
    def __init__(self, address: Address) -> None:
        self.address = address
        self.dials: list[tuple[str, int, str]] = []

    def connect_tcp(
        self,
        host: str,
        port: int,
        timeout: float | None = None,
        local_address: str | None = None,
        socket_options: object = None,
    ) -> DeadlineStream:
        if self.dials:
            raise httpcore.ConnectError("Second dial refused")
        self.dials.append((host, port, str(self.address)))
        deadline = time.monotonic() + 2
        family = socket.AF_INET6 if self.address.version == 6 else socket.AF_INET
        sock = socket.socket(family)
        try:
            sock.settimeout(min(timeout or 2, 2))
            sock.connect((str(self.address), port))
            if ipaddress.ip_address(sock.getpeername()[0]) != self.address:
                raise httpcore.ConnectError("Peer mismatch")
            return DeadlineStream(sock, deadline)
        except OSError as error:
            sock.close()
            raise httpcore.ConnectError("Fixture dial failed") from error
        except BaseException:
            sock.close()
            raise


def probe(context: ssl.SSLContext, dial: OneDial) -> httpx.Client:
    transport = httpx.HTTPTransport(
        verify=context,
        trust_env=False,
        http2=False,
        retries=0,
        limits=httpx.Limits(max_keepalive_connections=0),
    )
    transport._pool._network_backend = dial
    return httpx.Client(transport=transport, trust_env=False, follow_redirects=False, timeout=2)


def fixture_addresses() -> tuple[Address, ...]:
    addresses = {
        ipaddress.ip_address(answer[4][0].split("%")[0])
        for answer in socket.getaddrinfo(socket.gethostname(), None, type=socket.SOCK_STREAM)
    }
    ipv6_table = Path("/proc/net/if_inet6")
    if ipv6_table.exists():
        addresses.update(
            ipaddress.IPv6Address(int(line.split()[0], 16))
            for line in ipv6_table.read_text().splitlines()
        )
    selected: list[Address] = []
    for version in (4, 6):
        results = sorted(
            address
            for address in addresses
            if address.version == version and any(address in network for network in PRIVATE)
        )
        assert results, f"Isolated private IPv{version} fixture address is required"
        selected.append(results[0])
    return tuple(selected)


def tls_contexts(
    path: Path, addresses: tuple[Address, ...]
) -> tuple[ssl.SSLContext, ssl.SSLContext]:
    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "probe.test")])
    now = datetime.now(UTC)
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=1))
        .not_valid_after(now + timedelta(minutes=15))
        .add_extension(
            x509.SubjectAlternativeName(
                [x509.DNSName("probe.test"), *(x509.IPAddress(address) for address in addresses)]
            ),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )
    cert_file, key_file = path / "certificate.pem", path / "key.pem"
    cert_file.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    key_file.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    server = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    server.load_cert_chain(cert_file, key_file)
    client = ssl.create_default_context(cafile=str(cert_file))
    return server, client


@contextmanager
def endpoint(
    address: Address, context: ssl.SSLContext | None, redirect: str = "/unexpected"
) -> Iterator[tuple[int, list[str], list[str | None]]]:
    hosts: list[str] = []
    sni: list[str | None] = []

    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_GET(self) -> None:
            hosts.append(self.headers["Host"])
            if self.path == "/wait":
                time.sleep(2.5)
            self.send_response(302 if self.path == "/redirect" else 204)
            if self.path == "/redirect":
                self.send_header("Location", redirect)
            self.send_header("Content-Length", "0")
            try:
                self.end_headers()
            except OSError:
                if self.path != "/wait":
                    raise

        def log_message(self, format: str, *args: object) -> None:
            pass

    class Server(ThreadingHTTPServer):
        address_family = socket.AF_INET6 if address.version == 6 else socket.AF_INET

    with Server((str(address), 0), Handler) as server:
        if context:

            def record_sni(
                connection: ssl.SSLSocket, name: str | None, config: ssl.SSLContext
            ) -> None:
                sni.append(name)

            context.set_servername_callback(record_sni)
            server.socket = context.wrap_socket(server.socket, server_side=True)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield server.server_port, hosts, sni
        finally:
            server.shutdown()
            thread.join(timeout=3)


@contextmanager
def dns_fixture(
    answers: list[str],
    *,
    truncated: bool = False,
) -> Iterator[tuple[int, list[tuple[str, str]]]]:
    seen: list[tuple[str, str]] = []

    class Resolver(socketserver.BaseRequestHandler):
        def handle(self) -> None:
            wire, send = self.request
            query = dns.message.from_wire(wire)
            question = query.question[0]
            record_type = dns.rdatatype.to_text(question.rdtype)
            seen.append((str(question.name), record_type))
            response = dns.message.make_response(query)
            if truncated and record_type == "AAAA":
                response.flags |= dns.flags.TC
            matches = [
                answer
                for answer in answers
                if ipaddress.ip_address(answer).version == (4 if record_type == "A" else 6)
            ]
            if matches:
                response.answer.append(
                    dns.rrset.from_text(str(question.name), 1, "IN", record_type, *matches)
                )
            send.sendto(response.to_wire(), self.client_address)

    with socketserver.UDPServer(("127.0.0.1", 0), Resolver) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield server.server_address[1], seen
        finally:
            server.shutdown()
            thread.join(timeout=3)


def resolve(port: int) -> list[str]:
    answers = []
    deadline = time.monotonic() + 1
    for record_type in ("A", "AAAA"):
        request = dns.message.make_query("probe.test.", record_type)
        response = dns.query.udp(
            request, "127.0.0.1", port=port, timeout=max(0, deadline - time.monotonic())
        )
        if response.rcode() != 0 or response.flags & dns.flags.TC:
            raise Denied("DNS fixture resolution failed")
        answers.extend(str(entry) for rrset in response.answer for entry in rrset)
    return answers


def test_pinned_transport(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    addresses = fixture_addresses()
    protected = {ipaddress.ip_address("192.168.100.2")}
    for forbidden in ("127.0.0.1", "::1", "::ffff:127.0.0.1", "169.254.169.254", "192.168.100.2"):
        parsed = ipaddress.ip_address(forbidden)
        with pytest.raises(Denied):
            select([str(addresses[0]), forbidden], (*addresses, parsed), protected)
    with pytest.raises(Denied):
        select([], addresses, protected)

    for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"):
        monkeypatch.setenv(name, "http://127.0.0.1:1")
    monkeypatch.setenv("NO_PROXY", "")
    server_context, client_context = tls_contexts(tmp_path, addresses)

    with dns_fixture([str(addresses[0])], truncated=True) as (dns_port, _):
        with pytest.raises(Denied, match="resolution failed"):
            resolve(dns_port)

    for address in addresses:
        answers = [str(address)]
        with (
            endpoint(address, server_context) as (port, hosts, sni),
            dns_fixture(answers) as (dns_port, queries),
        ):
            selected = select(resolve(dns_port), addresses, protected)
            answers[:] = [str(address), "127.0.0.1"]
            dial = OneDial(selected)
            with probe(client_context, dial) as client:
                url = f"https://probe.test:{port}"
                response = client.get(url + "/redirect")
                assert response.status_code == 302 and not response.history
                assert hosts == [f"probe.test:{port}"] and sni == ["probe.test"]
                assert dial.dials == [("probe.test", port, str(address))]
                with pytest.raises(httpx.ConnectError, match="Second dial refused"):
                    client.get(url)
                assert len(hosts) == 1
            assert queries == [("probe.test.", "A"), ("probe.test.", "AAAA")]
            with pytest.raises(Denied):
                select(resolve(dns_port), addresses, protected)
            assert len(queries) == 4

            host = f"[{address}]" if address.version == 6 else str(address)
            with probe(client_context, OneDial(address)) as client:
                assert client.get(f"https://{host}:{port}").status_code == 204
            assert sni[-1] is None and hosts[-1] == f"{host}:{port}"
            expected_requests = len(hosts)
            for reference in ("wrong.test", "192.168.77.77"):
                with probe(client_context, OneDial(address)) as client:
                    with pytest.raises(httpx.ConnectError, match="TLS handshake"):
                        client.get(f"https://{reference}:{port}")
            assert len(hosts) == expected_requests

            dial = OneDial(address)
            with probe(client_context, dial) as client:
                started = time.monotonic()
                with pytest.raises(httpx.ReadTimeout):
                    client.get(f"https://probe.test:{port}/wait")
                assert time.monotonic() - started < 2.4
                assert len(dial.dials) == 1

        with endpoint(address, None) as (port, hosts, _):
            dial = OneDial(address)
            with probe(client_context, dial) as client:
                assert client.get(f"http://probe.test:{port}").status_code == 204
            assert hosts == [f"probe.test:{port}"]
        with probe(client_context, OneDial(address)) as client:
            with pytest.raises(httpx.ConnectError, match="Fixture dial failed"):
                client.get(f"http://probe.test:{port}")
        print(f"IPv{address.version}: pinned destination, Host, SNI, certificate, one dial")


def test_denied_direct_and_redirect_targets(tmp_path: Path) -> None:
    addresses = fixture_addresses()
    server_context, client_context = tls_contexts(tmp_path, addresses)
    for address in addresses:
        literal = f"[{address}]" if address.version == 6 else str(address)
        with endpoint(address, server_context) as (port, denied_hosts, _):
            location = f"https://{literal}:{port}/denied"
            forms = [str(address)]
            if address.version == 4:
                forms.append(f"::ffff:{address}")
            for form in forms:
                with pytest.raises(Denied, match="No internal allowlist match"):
                    select([form], (), set())
                with pytest.raises(Denied, match="Always denied"):
                    select([form], addresses, {address})

            with endpoint(address, server_context, location) as (allowed_port, hosts, _):
                selected = select([str(address)], addresses, set())
                dial = OneDial(selected)
                with probe(client_context, dial) as client:
                    response = client.get(f"https://probe.test:{allowed_port}/redirect")
                assert response.status_code == 302 and response.headers["Location"] == location
                assert dial.dials == [("probe.test", allowed_port, str(address))]
                assert len(hosts) == 1 and denied_hosts == []

    for forbidden in (
        "0.0.0.0",
        "::",
        "224.0.0.1",
        "::ffff:224.0.0.1",
        "ff02::1",
        "255.255.255.255",
        "fe80::1",
        "::ffff:169.254.169.254",
    ):
        # These values are classifier inputs only.
        parsed = ipaddress.ip_address(forbidden)
        with pytest.raises(Denied, match="Always denied"):
            select([str(addresses[0]), forbidden], (*addresses, parsed), set())
    print("Forbidden direct literals, redirects to denied listeners, and address conflicts passed")
