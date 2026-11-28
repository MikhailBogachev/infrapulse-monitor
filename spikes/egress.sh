#!/usr/bin/env bash
# Run on native Linux in fresh mount and network namespaces.
set -Eeuo pipefail
if [[ $(uname -s) != Linux || $EUID != 0 || ${1:-} == "" ]]; then
  echo "Use the documented isolated Linux invocation." >&2
  exit 2
fi
for namespace in net mnt; do
  if [[ $(readlink "/proc/self/ns/$namespace") == $(readlink "/proc/1/ns/$namespace") ]]; then
    echo "Refusing to operate in the host $namespace namespace." >&2
    exit 2
  fi
done
links=$(ip -o link show)
if [[ $(readlink /proc/self/ns/net) == "$1" ]] ||
   awk -F ': ' '$2 && $2 != "lo" { found=1 } END { exit !found }' <<<"$links"; then
  echo "Refusing a network namespace with an existing network attachment." >&2
  exit 2
fi
unset DOCKER_CONTEXT
export DOCKER_HOST=unix:///var/run/docker.sock
engine_os=$(docker info --format '{{.OperatingSystem}}')
if [[ $engine_os == *"Docker Desktop"* ]]; then
  echo "This experiment requires native Linux Docker Engine." >&2
  exit 2
fi

mount --make-rprivate /
fixture=$(dirname "$(realpath "$0")")/egress_fixture.py
image=python:3.13.12-slim-bookworm
pids=()
worker=
worker_pid=
run_id=$(cat /proc/sys/kernel/random/uuid)
echo "Synthetic fixture run=$run_id pid=$$ netns=$(readlink /proc/self/ns/net) mountns=$(readlink /proc/self/ns/mnt)"
nft --version
ip -Version
cleanup() {
  local status=$?
  trap - EXIT
  if (( status != 0 )); then
    nft list ruleset || true
    if [[ -n $worker ]]; then
      if [[ -n $worker_pid ]]; then nsenter -t "$worker_pid" -n nft list ruleset || true; fi
      docker logs "$worker" || true
    fi
  fi
  if [[ -n $worker ]]; then
    if [[ $(docker inspect -f '{{.State.Running}}' "$worker") == true ]]; then
      docker stop -t 3 "$worker" >/dev/null || status=1
      local code
      code=$(docker wait "$worker") || status=1
      echo "Stopped generation=$worker exit=$code"
      [[ $code == 0 ]] || status=1
      docker logs --tail 2 "$worker" || status=1
    fi
    docker rm -f "$worker" >/dev/null || status=1
  fi
  for pid in "${pids[@]}"; do kill "$pid" 2>/dev/null || true; done
  for pid in "${pids[@]}"; do
    if ! wait "$pid"; then
      echo "Fixture did not exit cleanly pid=$pid" >&2
      status=1
    fi
    echo "Fixture reaped pid=$pid"
  done
  exit "$status"
}
trap cleanup EXIT
trap 'echo "Synthetic assertion/command failed at line $LINENO: $BASH_COMMAND" >&2' ERR
trap 'exit 130' INT
trap 'exit 143' TERM

ip link set lo up
sysctl -qw net.ipv4.ip_forward=1 net.ipv6.conf.all.forwarding=1

attach() {
  local pid=$1 subnet=$2 host=$3 router="router$2"
  local link=$router
  if [[ $subnet == 70 ]]; then link=worker70; fi
  ip link add "$link" type veth peer name edge
  ip link set edge netns "$pid"
  if [[ $subnet == 70 ]]; then
    ip link set "$link" master "$router"
  else
    gateway_addresses "$subnet" "$router"
  fi
  ip link set "$link" up
  nsenter -t "$pid" -n ip addr add "10.$subnet.0.$host/24" dev edge
  nsenter -t "$pid" -n ip -6 addr add "fd00:$subnet::$host/64" dev edge nodad
  nsenter -t "$pid" -n ip link set edge up
  nsenter -t "$pid" -n ip route add default via "10.$subnet.0.1"
  nsenter -t "$pid" -n ip -6 route add default via "fd00:$subnet::1"
}

gateway_addresses() {
  local subnet=$1 router=$2
  ip addr add "10.$subnet.0.1/24" dev "$router"
  ip -6 addr add "fd00:$subnet::1/64" dev "$router" nodad
}

endpoint() {
  local subnet=$1 role=$2 ipv4=$3 ipv6=$4
  shift 4
  unshare --net -- python3 "$fixture" serve "$run_id-$role" "$ipv4" "$ipv6" "$@" &
  local pid=$!
  pids+=("$pid")
  local deadline=$((SECONDS+5))
  local namespace
  until namespace=$(readlink "/proc/$pid/ns/net") &&
    [[ $namespace != "$(readlink /proc/self/ns/net)" ]]; do
    (( SECONDS < deadline ))
    sleep 0.05
  done
  echo "Fixture attached identity=$run_id-$role pid=$pid netns=$namespace"
  attach "$pid" "$subnet" 2
  python3 "$fixture" ready "$run_id-$role" "$ipv4" "$ipv6" "$@"
}

apply_ruleset() {
  local ruleset
  ruleset=$(cat)
  "$@" nft --check -f - <<<"$ruleset"
  "$@" nft -f - <<<"$ruleset"
}

apply_ruleset <<'RULES'
table inet ip007_gateway {
  counter host_drops {}
  counter translated_v4 {}
  counter translated_v6 {}
  chain translate {
    type nat hook prerouting priority dstnat; policy accept;
    iifname "router70" ip daddr 10.71.0.99 tcp dport 18080 dnat ip to 10.72.0.2
    iifname "router70" ip6 daddr fd00:71::99 tcp dport 18080 dnat ip6 to fd00:72::2
  }
  chain local_input {
    type filter hook input priority filter; policy accept;
    iifname "router70" meta l4proto tcp counter name host_drops drop
  }
  chain transit {
    type filter hook forward priority filter; policy drop;
    ct state established,related accept
    iifname "router70" ip daddr 10.72.0.2 tcp dport 18082 accept
    iifname "router70" ip6 daddr fd00:72::2 tcp dport 18082 accept
    iifname "router70" ip daddr 10.72.0.0/24 counter name translated_v4 drop
    iifname "router70" ip6 daddr fd00:72::/64 counter name translated_v6 drop
    iifname "router70" ip daddr 10.71.0.0/24 tcp dport 18080 accept
    iifname "router70" ip6 daddr fd00:71::/64 tcp dport 18080 accept
  }
}
RULES

endpoint 71 allowed 10.71.0.2 fd00:71::2 18080
endpoint 72 control 10.72.0.2 fd00:72::2 18080 18082
endpoint 73 blocked 10.73.0.2 fd00:73::2 18080

worker_fixture() {
  docker exec "$worker" python /fixture.py "$@"
}

provision() {
  local host=$1
  local status=0
  worker=$(docker create --pull never --network none --cap-drop ALL \
    --security-opt no-new-privileges --read-only --user 10001:10001 \
    --tmpfs /tmp:rw,noexec,nosuid,nodev \
    --mount "type=bind,source=$fixture,target=/fixture.py,readonly" \
    "$image" python -u /fixture.py watch-startup)
  docker start "$worker" >/dev/null
  worker_pid=$(docker inspect -f '{{.State.Pid}}' "$worker")
  [[ $(docker inspect -f '{{.HostConfig.NetworkMode}}' "$worker") == none ]]
  [[ $(readlink "/proc/$worker_pid/ns/net") != $(readlink /proc/self/ns/net) ]]
  [[ $(nsenter -t "$worker_pid" -n ip -o link show | wc -l) == 1 ]]
  nsenter -t "$worker_pid" -n sysctl -qw net.ipv6.conf.all.disable_ipv6=0
  worker_fixture wait-startup
  worker_fixture disconnected
  worker_fixture check-after-policy "$run_id" || status=$?
  [[ $status == 3 ]]
  echo "Container $worker starts disconnected pid=$worker_pid netns=$(readlink "/proc/$worker_pid/ns/net")"

  # The host controls this namespace; the test process has no network capabilities.
  apply_ruleset nsenter -t "$worker_pid" -n <<'RULES'
table inet ip007_worker_v1 {
  counter local_drops {}
  counter denied_v4 {}
  counter denied_v6 {}
  counter default_drops {}
  chain out {
    type filter hook output priority filter; policy drop;
    oifname "lo" counter name local_drops drop
    ip6 hoplimit 255 icmpv6 type { nd-neighbor-solicit, nd-neighbor-advert } accept
    ct state established,related accept
    ip daddr 10.72.0.2 tcp dport 18082 accept
    ip6 daddr fd00:72::2 tcp dport 18082 accept
    ip daddr 10.72.0.0/24 counter name denied_v4 drop
    ip6 daddr fd00:72::/64 counter name denied_v6 drop
    ip daddr { 10.71.0.0/24, 10.72.0.0/24, 10.70.0.1 } tcp dport 18080 accept
    ip6 daddr { fd00:71::/64, fd00:72::/64, fd00:70::1 } tcp dport 18080 accept
    counter name default_drops drop
  }
}
RULES
  nsenter -t "$worker_pid" -n nft list chain inet ip007_worker_v1 out
  worker_fixture arm
  worker_fixture sealed
  attach "$worker_pid" 70 "$host"
  nsenter -t "$worker_pid" -n ip -br addr show edge
  [[ $(nsenter -t "$worker_pid" -n ip -4 -o addr show dev edge) == *"10.70.0.$host/24"* ]]
  [[ $(nsenter -t "$worker_pid" -n ip -6 -o addr show dev edge) == *"fd00:70::$host/64"* ]]
  worker_fixture mark-ready
  echo "Policy ready generation=$worker version=ip007_worker_v1"
}

# The gateway owns its addresses and listeners throughout worker replacement.
ip link add router70 type bridge
gateway_addresses 70 router70
ip link set router70 up
python3 "$fixture" serve "$run_id-gateway" 10.70.0.1 fd00:70::1 18080 &
pids+=("$!")
python3 "$fixture" ready "$run_id-gateway" 10.70.0.1 fd00:70::1 18080

coverage() {
  local counter
  worker_fixture check-after-policy "$run_id"
  for counter in local_drops denied_v4 denied_v6 default_drops; do
    nsenter -t "$worker_pid" -n nft list counter inet ip007_worker_v1 "$counter" |
      grep -E 'packets [1-9][0-9]*'
  done
  nft list table inet ip007_gateway
  worker_fixture finish-startup
  docker logs "$worker"
}

provision 2
coverage
for counter in host_drops translated_v4 translated_v6; do
  nft list counter inet ip007_gateway "$counter" | grep -E 'packets [1-9][0-9]*'
  nft reset counter inet ip007_gateway "$counter" >/dev/null
done

old=$worker
old_namespace=$(readlink "/proc/$worker_pid/ns/net")
docker stop -t 1 "$old" >/dev/null
echo "Stopped generation=$old netns=$old_namespace exit=$(docker wait "$old")"
[[ $(docker inspect -f '{{.State.Status}} {{.State.Pid}} {{.State.ExitCode}}' "$old") == 'exited 0 0' ]]
docker logs --tail 2 "$old"
docker rm "$old" >/dev/null
worker=
# Kernel teardown removes both ends when the removed Docker namespace is released.
deadline=$((SECONDS+5))
while ip link show dev worker70 >/dev/null 2>&1; do
  if (( SECONDS >= deadline )); then
    echo "The old worker attachment survived removal." >&2
    exit 1
  fi
  sleep 0.05
done
provision 3
python3 "$fixture" ready "$run_id-gateway" 10.70.0.1 fd00:70::1 18080
[[ $worker != "$old" && $(readlink "/proc/$worker_pid/ns/net") != "$old_namespace" ]]
coverage
for counter in host_drops translated_v4 translated_v6; do
  nft list counter inet ip007_gateway "$counter" | grep -E 'packets [1-9][0-9]*'
done
