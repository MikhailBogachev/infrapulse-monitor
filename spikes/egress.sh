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
worker_start=
worker_namespace=
worker_digest=
old=
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
      local pid
      pid=$(docker inspect -f '{{.State.Pid}}' "$worker") || pid=0
      if [[ $pid != 0 ]]; then nsenter -t "$pid" -n nft list ruleset || true; fi
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

process_start() {
  python3 "$fixture" process-start "$1"
}

live_worker_policy() {
  [[ $(docker inspect -f '{{.State.Running}} {{.State.Pid}}' "$worker") == "true $worker_pid" ]]
  [[ $(process_start "$worker_pid") == "$worker_start" ]]
  [[ $(readlink "/proc/$worker_pid/ns/net") == "$worker_namespace" ]]
  local digest
  digest=$(nsenter -t "$worker_pid" -n nft -s list table inet ip007_worker_v1 | sha256sum)
  [[ $digest == "$worker_digest" ]]
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
  [[ $worker_pid != 0 ]]
  worker_start=$(process_start "$worker_pid")
  [[ -n $worker_start ]]
  worker_namespace=$(readlink "/proc/$worker_pid/ns/net")
  if [[ -n $old ]]; then
    python3 "$fixture" verify-replacement "$old" "$old_pid" "$old_start" \
      "$worker" "$worker_pid" "$worker_start"
  fi
  [[ $(docker inspect -f '{{.HostConfig.NetworkMode}}' "$worker") == none ]]
  [[ $(docker inspect -f '{{.HostConfig.PidMode}}' "$worker") == '' ]]
  [[ $worker_namespace != "$(readlink /proc/self/ns/net)" ]]
  [[ $worker_namespace != "$(readlink /proc/1/ns/net)" ]]
  [[ $(nsenter -t "$worker_pid" -n ip -o link show | wc -l) == 1 ]]
  nsenter -t "$worker_pid" -n sysctl -qw net.ipv6.conf.all.disable_ipv6=0
  worker_fixture wait-startup
  worker_fixture disconnected
  worker_fixture check-after-policy "$run_id" "$worker" || status=$?
  [[ $status == 3 ]]
  local tables
  tables=$(nsenter -t "$worker_pid" -n nft list tables)
  if grep -Fxq 'table inet ip007_worker_v1' <<<"$tables"; then
    echo "Worker policy survived container creation: generation=$worker" >&2
    return 1
  fi
  echo "Container $worker starts disconnected pid=$worker_pid start=$worker_start netns=$worker_namespace sandbox=$(docker inspect -f '{{.NetworkSettings.SandboxKey}}' "$worker")"

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
  worker_digest=$(nsenter -t "$worker_pid" -n nft -s list table inet ip007_worker_v1 | sha256sum)
  worker_fixture arm
  worker_fixture sealed
  attach "$worker_pid" 70 "$host"
  nsenter -t "$worker_pid" -n ip -br addr show edge
  [[ $(nsenter -t "$worker_pid" -n ip -4 -o addr show dev edge) == *"10.70.0.$host/24"* ]]
  [[ $(nsenter -t "$worker_pid" -n ip -6 -o addr show dev edge) == *"fd00:70::$host/64"* ]]
  live_worker_policy
  worker_fixture mark-ready "$worker"
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
  live_worker_policy
  worker_fixture check-after-policy "$run_id" "$worker"
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
old_pid=$worker_pid
old_start=$worker_start
live_worker_policy
docker stop -t 1 "$old" >/dev/null
code=$(docker wait "$old")
[[ $code == 0 ]]
[[ $(docker inspect -f '{{.State.Status}} {{.State.Pid}} {{.State.ExitCode}}' "$old") == 'exited 0 0' ]]
echo "Stopped generation=$old pid=$old_pid start=$old_start exit=$code"
docker logs --tail 2 "$old"
docker rm "$old" >/dev/null
worker=
# The kernel can recycle both IDs after teardown. Keep no namespace FD or mount
# alive here, and require the previous process and veth to be gone before create.
deadline=$((SECONDS+5))
while true; do
  current_start=$(process_start "$old_pid")
  links=$(ip -o link show)
  if [[ $current_start != "$old_start" ]] &&
     ! grep -Eq '^[0-9]+: worker70(@[^:]+)?:' <<<"$links"; then
    break
  fi
  if (( SECONDS >= deadline )); then
    echo "The old process or its attachment survived removal: generation=$old pid=$old_pid start=$old_start" >&2
    exit 1
  fi
  sleep 0.05
done
provision 3
python3 "$fixture" ready "$run_id-gateway" 10.70.0.1 fd00:70::1 18080
coverage
for counter in host_drops translated_v4 translated_v6; do
  nft list counter inet ip007_gateway "$counter" | grep -E 'packets [1-9][0-9]*'
done
