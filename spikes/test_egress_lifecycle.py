"""Exercise foreground listener ownership using an actual fixture process."""

import errno
import socket
import subprocess
import sys
from pathlib import Path

import pytest
from egress_fixture import policy_ready, ready, verify_replacement

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


def write_process(proc: Path, pid: int, start: int, netns: str) -> None:
    directory = proc / str(pid)
    (directory / "ns").mkdir(parents=True, exist_ok=True)
    (directory / "stat").write_text(f"{pid} (worker ) process) S {'0 ' * 18}{start} 0\n")
    link = directory / "ns/net"
    link.unlink(missing_ok=True)
    link.symlink_to(netns)


@pytest.mark.parametrize("new_pid", [3425, 3856])
def test_replacement_accepts_recycled_namespace_id(tmp_path: Path, new_pid: int) -> None:
    old_pid = 3425
    write_process(tmp_path, old_pid, 100, "net:[4026532513]")
    old_link = tmp_path / str(old_pid) / "ns/net"
    old_namespace = old_link.readlink()
    old_link.unlink()
    (tmp_path / str(old_pid) / "stat").unlink()

    write_process(tmp_path, new_pid, 200, "net:[4026532513]")
    assert (tmp_path / str(new_pid) / "ns/net").readlink() == old_namespace
    verify_replacement("old", old_pid, "100", "new", new_pid, "200", tmp_path)


def test_replacement_rejects_live_predecessor_and_wrong_successor(tmp_path: Path) -> None:
    write_process(tmp_path, 10, 100, "net:[1]")
    write_process(tmp_path, 20, 200, "net:[2]")
    with pytest.raises(AssertionError, match="Previous process still exists"):
        verify_replacement("old", 10, "100", "new", 20, "200", tmp_path)
    (tmp_path / "10/stat").unlink()
    with pytest.raises(AssertionError, match="Replacement process changed"):
        verify_replacement("old", 10, "100", "new", 20, "199", tmp_path)
    with pytest.raises(AssertionError, match="reused the previous container"):
        verify_replacement("old", 10, "100", "old", 20, "200", tmp_path)


def test_policy_readiness_belongs_to_container_generation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    marker = tmp_path / "ready"
    monkeypatch.setattr("egress_fixture.READY", marker)
    assert not policy_ready("new")
    marker.write_text("old")
    assert not policy_ready("new")
    marker.write_text("new")
    assert policy_ready("new")
