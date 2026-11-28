"""Exercise foreground listener ownership using an actual fixture process."""

import errno
import socket
import subprocess
import sys
from pathlib import Path

import pytest
from egress_fixture import ready

FIXTURE = Path(__file__).with_name("egress_fixture.py")
ADDRESSES = ("127.0.0.1", "::1")


def command(identity: str, port: int) -> list[str]:
    return [sys.executable, str(FIXTURE), "serve", identity, *ADDRESSES, str(port)]


def test_keep_same_listener_across_generations_and_stop() -> None:
    with socket.socket() as reservation:
        reservation.bind((ADDRESSES[0], 0))
        port = reservation.getsockname()[1]
    with subprocess.Popen(command("gateway-run", port), stdout=subprocess.PIPE, text=True) as child:
        try:
            for _ in range(2):
                ready("gateway-run", ADDRESSES, (port,))
                assert child.poll() is None
            with pytest.raises(AssertionError, match="Fixture identity mismatch"):
                ready("different-run", ADDRESSES, (port,))
        finally:
            child.terminate()
            try:
                output, _ = child.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                child.kill()
                child.communicate()
                raise
        assert child.returncode == 0
        assert f"Fixture starting identity=gateway-run pid={child.pid}" in output
        assert output.count("Fixture ready") == 1
        assert f"Fixture stopped identity=gateway-run pid={child.pid}" in output


def test_bind_failure_exits_and_releases_previously_bound_socket() -> None:
    with socket.socket(socket.AF_INET6) as conflict:
        conflict.bind((ADDRESSES[1], 0))
        conflict.listen()
        port = conflict.getsockname()[1]
        result = subprocess.run(
            command("conflict", port), capture_output=True, text=True, timeout=5
        )
        assert result.returncode == 1
        assert "Fixture ready" not in result.stdout
        assert "Fixture stopped identity=conflict" in result.stdout
        assert "Bind failed" in result.stderr
        assert f"[Errno {errno.EADDRINUSE}]" in result.stderr
        with socket.socket() as released:
            released.bind((ADDRESSES[0], port))
