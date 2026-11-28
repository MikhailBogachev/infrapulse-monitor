"""Exercise the publication verdict with controlled packet-counter observations."""

import os
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).with_name("topology_network.sh")


@pytest.mark.parametrize("family", [4, 6])
@pytest.mark.parametrize(
    ("scenario", "passed"),
    [
        ("correct-dnat", True),
        ("timeout-without-ingress", False),
        ("timeout-without-dnat", False),
        ("denied-syn-reached-listener", False),
        ("control-missed-dnat", False),
        ("control-missed-listener", False),
        ("unexpected-connection", False),
    ],
)
def test_publication_verdict(tmp_path: Path, family: int, scenario: str, passed: bool) -> None:
    state = tmp_path / "probe-state"
    state.write_text("initial\n")
    result = subprocess.run(
        [
            "bash",
            "-euo",
            "pipefail",
            "-c",
            """
            source "$1"
            conntrack() { :; }
            ip() {
              if [[ $* == *"--local-port $control_port "* ]]; then
                echo control > "$state"
                return 0
              fi
              [[ $* == *"--local-port $denied_port "* ]] || return 2
              echo denied > "$state"
              if [[ $scenario == unexpected-connection ]]; then return 0; fi
              return 28
            }
            nsenter() {
              [[ $1 == -t && $2 == "$nginx_pid" && $3 == -n ]] || return 2
              shift 3
              nginx_namespace=1 "$@"
            }
            nft() {
              local count=3
              [[ $* == "list counter inet $table "*_v"$family" ]] || return 2
              if [[ $5 == received_* && ${nginx_namespace:-0} != 1 ]]; then return 2; fi
              case "$(cat "$state"):$5" in
                control:control_*|denied:control_*)
                  if [[ $scenario != control-missed-dnat ]]; then count=4; fi;;
                denied:ingress_*)
                  if [[ $scenario != timeout-without-ingress ]]; then count=4; fi;;
                denied:published_*)
                  if [[ $scenario != timeout-without-dnat ]]; then count=4; fi;;
                control:received_*|denied:received_*)
                  if [[ $scenario != control-missed-listener ]]; then count=4; fi
                  if [[ $(cat "$state") == denied && $scenario == denied-syn-reached-listener ]]
                  then count=5; fi;;
              esac
              printf 'packets %s bytes 240\n' "$count"
            }
            verify_publication "$family"
            """,
            "test-publication",
            str(SCRIPT),
        ],
        env={
            **os.environ,
            "COMPOSE_PROJECT_NAME": "topology-test",
            "table": "ip007_test",
            "nginx_pid": "42",
            "nginx_v4": "192.0.2.3",
            "nginx_v6": "2001:db8::3",
            "family": str(family),
            "scenario": scenario,
            "state": str(state),
        },
        capture_output=True,
        text=True,
        timeout=5,
    )
    assert (result.returncode == 0) == passed, result.stdout + result.stderr


def test_source_ports_are_distinct() -> None:
    result = subprocess.run(
        [
            "bash",
            "-euo",
            "pipefail",
            "-c",
            'source "$1"; printf "%s\n" "${control_ports[@]}" "${denied_ports[@]}"',
            "test-publication",
            str(SCRIPT),
        ],
        env={**os.environ, "COMPOSE_PROJECT_NAME": "topology-test", "table": "ip007_test"},
        check=True,
        capture_output=True,
        text=True,
        timeout=5,
    )
    assert len(set(result.stdout.splitlines())) == 4
