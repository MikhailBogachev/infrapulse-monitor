#!/usr/bin/env bash
# Run only on a disposable native Linux host with a local rootful Docker Engine.
set -Eeuo pipefail
if [[ $(uname -s) != Linux || $EUID != 0 ]]; then
  echo "Use sudo make spike-topology on a disposable native Linux host." >&2
  exit 2
fi
unset DOCKER_CONTEXT
export DOCKER_HOST=unix:///var/run/docker.sock
engine=$(docker info --format '{{.OperatingSystem}} {{.CgroupVersion}}')
if [[ $engine == *"Docker Desktop"* || $engine != *" 2" ]]; then
  echo "Native Docker Engine with cgroup v2 is required (found $engine)." >&2
  exit 2
fi
for bridge in ip007-control ip007-check ip007-provider; do
  if ip link show "$bridge" >/dev/null 2>&1; then
    echo "Existing fixture bridge: $bridge" >&2
    exit 2
  fi
done

repo=$(dirname "$(dirname "$(realpath "$0")")")
cd "$repo"
IP007_LAB=$(mktemp -d)
export IP007_LAB
export COMPOSE_PROJECT_NAME="ip007-topology-${IP007_LAB##*.}"
export COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME,,}
export INFRAPULSE_SECRETS_DIR="$IP007_LAB/secrets"
base=(docker compose -f compose.yaml)
compose=("${base[@]}" -f spikes/topology.compose.yaml)
table="ip007_${COMPOSE_PROJECT_NAME##*-}"
host_rules=0
wire_rules=0
host_digest=
nginx_pid=
source spikes/topology_network.sh
declare -A worker_digests
host_listener=
checks=
notifications=
safe_logs() {
  docker logs --tail 100 "$1" 2>&1 |
    python3 spikes/topology_diagnostics.py "$INFRAPULSE_SECRETS_DIR" "$IP007_LAB/tls/key.pem"
}

cleanup() {
  local status=$?
  trap - EXIT
  stop_publication_trace || status=1
  if (( listener_rules )); then
    nsenter -t "$nginx_pid" -n nft list table inet "$table" || status=1
  fi
  if (( status && host_rules )); then
    publication_snapshot || true
  fi
  if (( host_rules )); then
    nft list table inet "$table" || status=1
  fi
  if (( wire_rules )); then
    nft list table bridge "$table" || status=1
  fi
  for container in "$checks" "$notifications"; do
    if [[ -n $container ]]; then
      local pid
      pid=$(docker inspect -f '{{.State.Pid}}' "$container" 2>/dev/null) || pid=0
      if [[ $pid != 0 ]]; then
        nsenter -t "$pid" -n nft list table inet ip007_worker || status=1
      fi
    fi
  done
  "${compose[@]}" ps -a || status=1
  local services=(worker-checks worker-notifications check-target provider-target denied-target nginx)
  if (( status )); then services+=(postgres rabbitmq redis migrate api scheduler); fi
  for service in "${services[@]}"; do
    local id
    id=$("${compose[@]}" ps -a -q "$service") || status=1
    if [[ -n $id ]]; then safe_logs "$id" || status=1; fi
  done
  if [[ -n $host_listener ]]; then
    kill "$host_listener" 2>/dev/null || true
    wait "$host_listener" || status=1
    echo "Host fixture reaped pid=$host_listener"
  fi
  if (( probe_namespace )); then ip netns delete "$probe_ns" || status=1; fi
  "${compose[@]}" down -v || status=1
  if (( host_rules )); then nft delete table inet "$table" || status=1; fi
  if (( wire_rules )); then nft delete table bridge "$table" || status=1; fi
  rm -rf -- "$IP007_LAB"
  exit "$status"
}
trap cleanup EXIT
trap 'echo "Compose assertion/command failed at line $LINENO: $BASH_COMMAND" >&2' ERR
trap 'exit 130' INT
trap 'exit 143' TERM

mkdir -m 755 "$IP007_LAB/admission" "$IP007_LAB/tls"
chmod 755 "$IP007_LAB"
python3 scripts/setup_secrets.py "$INFRAPULSE_SECRETS_DIR"
openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:P-256 -nodes -days 1   -subj /CN=probe.test -addext subjectAltName=DNS:probe.test   -keyout "$IP007_LAB/tls/key.pem" -out "$IP007_LAB/tls/certificate.pem"
chmod 444 "$IP007_LAB/tls/key.pem"
cp "$IP007_LAB/tls/certificate.pem" "$IP007_LAB/admission/"
sed 's/listen 8080;/listen 8080;\n    listen [::]:8080;/'   infra/nginx/default.conf > "$IP007_LAB/nginx.conf"

echo "Compose verification project=$COMPOSE_PROJECT_NAME engine=$engine"
docker version --format '{{.Server.Version}}'
docker compose version
nft --version
iptables --version
ip6tables --version
"${compose[@]}" config -q
"${compose[@]}" build api nginx
"${base[@]}" -f spikes/compose.yaml --profile spike build spike
"${compose[@]}" up -d --wait --wait-timeout 120 postgres rabbitmq redis migrate api scheduler
"${compose[@]}" up -d check-target provider-target denied-target
"${compose[@]}" up -d --wait --wait-timeout 45 nginx

apply() {
  local rules
  rules=$(cat)
  "$@" nft --check -f - <<<"$rules"
  "$@" nft -f - <<<"$rules"
}

nginx=$("${compose[@]}" ps -q nginx)
edge="{{with index .NetworkSettings.Networks \"${COMPOSE_PROJECT_NAME}_edge\"}}"
read -r nginx_v4 nginx_v6 < <(docker inspect -f "$edge{{.IPAddress}} {{.GlobalIPv6Address}}{{end}}" "$nginx")
[[ -n $nginx_v4 && -n $nginx_v6 ]]
nginx_pid=$(docker inspect -f '{{.State.Pid}}' "$nginx")
host_policy
host_rules=1
host_digest=$(nft -s list table inet "$table" | sha256sum)

# Compose attaches the bridges before starting the entrypoint. Quarantine the
# fixed worker addresses before Docker creates either generation.
apply <<RULES
table bridge $table {
  set held_v4 { type ipv4_addr; elements = { 10.213.50.10, 10.213.50.11, 10.213.51.10, 10.213.52.11 }; }
  set held_v6 { type ipv6_addr; elements = { fd42:213:50::10, fd42:213:50::11, fd42:213:51::10, fd42:213:52::11 }; }
  counter held_ipv4 {}
  counter held_ipv6 {}
  chain startup {
    type filter hook prerouting priority filter; policy accept;
    meta ibrname { "ip007-control", "ip007-check", "ip007-provider" } ip saddr @held_v4 meta l4proto { tcp, udp } counter name held_ipv4 drop
    meta ibrname { "ip007-control", "ip007-check", "ip007-provider" } ip6 saddr @held_v6 meta l4proto { tcp, udp } counter name held_ipv6 drop
  }
}
RULES
wire_rules=1

wire_gate() {
  local operation=$1 segment=$2 address=$3
  apply <<RULES
$operation element bridge $table held_v4 { 10.213.50.$address, 10.213.$segment.$address }
$operation element bridge $table held_v6 { fd42:213:50::$address, fd42:213:$segment::$address }
RULES
  echo "Startup quarantine action=$operation segment=$segment address=$address"
}

wait_log() {
  local container=$1 pattern=$2 deadline=$((SECONDS+25))
  until docker logs "$container" 2>&1 | grep -E "$pattern" >/dev/null; do
    [[ $(docker inspect -f '{{.State.Running}}' "$container") == true ]]
    if (( SECONDS >= deadline )); then
      echo "Missing event in $container: $pattern" >&2
      return 1
    fi
    sleep 0.1
  done
}

for service in check-target provider-target denied-target; do
  peer=$("${compose[@]}" ps -q "$service")
  wait_log "$peer" target-ready
  [[ $(docker inspect -f '{{.State.Running}}' "$peer") == true ]]
done
target=$("${compose[@]}" ps -q check-target)
python3 spikes/egress_fixture.py serve "$COMPOSE_PROJECT_NAME-host" 10.213.51.1 fd42:213:51::1 18081 &
host_listener=$!
python3 spikes/egress_fixture.py ready "$COMPOSE_PROJECT_NAME-host" 10.213.51.1 fd42:213:51::1 18081
# Exercise the actual Nginx publication from the host before worker assertions.
for host in '10.213.51.1' '[fd42:213:51::1]'; do
  curl --noproxy '*' -fsS --max-time 3 "http://$host:18080/health/live"
done

fixture() {
  local container=$1
  shift
  docker exec "$container" python /spikes/topology_fixture.py "$@"
}

start_worker() {
  local role=$1 variable=$2 container
  "${compose[@]}" up -d --no-deps --force-recreate "worker-$role"
  container=$("${compose[@]}" ps -q "worker-$role")
  [[ -n $container ]]
  printf -v "$variable" '%s' "$container"
  echo "Started gate role=$role id=$container pid=$(docker inspect -f '{{.State.Pid}}' "$container")"
}

worker_rules() {
  local container=$1 role=$2 pid segment permitted exceptions=
  pid=$(docker inspect -f '{{.State.Pid}}' "$container")
  segment=51
  permitted='
    ip daddr 10.213.51.0/24 tcp dport 443 accept
    ip6 daddr fd42:213:51::/64 tcp dport 443 accept'
  if [[ $role == notifications ]]; then
    segment=52
    permitted='
    ip daddr 10.213.52.2 tcp dport 443 accept
    ip6 daddr fd42:213:52::2 tcp dport 443 accept'
  fi
  if [[ $role == checks ]]; then
    # Allow the gateway paths here so that the host input and post-DNAT hooks
    # must make the denial observed by the test.
    exceptions='
    ip daddr 10.213.51.1 tcp dport { 18080, 18081 } accept
    ip6 daddr fd42:213:51::1 tcp dport { 18080, 18081 } accept'
  fi
  # Docker DNATs resolver requests in OUTPUT. Resolver replies traverse OUTPUT
  # too, before the reverse translation in POSTROUTING.
  apply nsenter -t "$pid" -n <<RULES
table inet ip007_worker {
  counter always_deny {}
  counter default_deny {}
  counter dns {}
  counter dns_reply {}
  chain out {
    type filter hook output priority filter; policy drop;
    oifname "lo" ip daddr 127.0.0.11 ct direction original ct status dnat meta l4proto { tcp, udp } ct original proto-dst 53 counter name dns accept
    oifname "lo" ip saddr 127.0.0.11 ct direction reply ct state established ct status dnat meta l4proto { tcp, udp } ct original ip daddr 127.0.0.11 ct original proto-dst 53 counter name dns_reply accept
    oifname "lo" counter name always_deny drop
    ip6 hoplimit 255 icmpv6 type { nd-neighbor-solicit, nd-neighbor-advert } accept
    ct state established,related accept
    ip daddr 10.213.$segment.2 meta skuid 0 meta l4proto { tcp, udp } th dport 53 accept
    ip daddr 10.213.50.2 tcp dport 5432 accept
    ip6 daddr fd42:213:50::2 tcp dport 5432 accept
    ip daddr 10.213.50.3 tcp dport 5672 accept
    ip6 daddr fd42:213:50::3 tcp dport 5672 accept
    ip daddr 10.213.50.0/24 counter name always_deny drop
    ip6 daddr fd42:213:50::/64 counter name always_deny drop
    ip daddr 10.213.$segment.3 counter name always_deny drop
    ip6 daddr fd42:213:$segment::3 counter name always_deny drop
    $exceptions
    $permitted
    counter name default_deny drop
  }
}
RULES
  nsenter -t "$pid" -n nft list table inet ip007_worker
  worker_digests[$container]=$(nsenter -t "$pid" -n nft -s list table inet ip007_worker | sha256sum)
}

policy() {
  local container=$1 role=$2 previous=$3 version=$4 lifetime=$5 pid namespace hostname
  pid=$(docker inspect -f '{{.State.Pid}}' "$container")
  hostname=$(docker inspect -f '{{.Config.Hostname}}' "$container")
  namespace=$(readlink "/proc/$pid/ns/net")
  if [[ $version == ip007-compose-v1 && $lifetime -gt 0 ]]; then
    local current_worker current_host
    if ! current_worker=$(nsenter -t "$pid" -n nft -s list table inet ip007_worker | sha256sum) ||
       ! current_host=$(nft -s list table inet "$table" | sha256sum) ||
       [[ $current_worker != "${worker_digests[$container]:-}" || $current_host != "$host_digest" ]]; then
      echo "Refused to publish readiness for generation=$container: live rules missing or stale"
      return 4
    fi
    echo "Verified live policy worker=$current_worker host=$current_host"
  fi
  local expires
  expires=$(($(date +%s) + lifetime))
  printf '{"hostname":"%s","netns":"%s","version":"%s","expires":%s,"previous":"%s"}\n' \
    "$hostname" "$namespace" "$version" "$expires" "$previous" > "$IP007_LAB/admission/staged"
  mv "$IP007_LAB/admission/staged" "$IP007_LAB/admission/$role.json"
  echo "Policy generation=$container pid=$pid netns=$namespace revision=$version expires=$expires previous=$previous"
}

refuse() {
  local container=$1 role=$2 label=$3 reason=$4 status=0 output before events peer
  peer=$target
  if [[ $role == notifications ]]; then peer=$("${compose[@]}" ps -q provider-target); fi
  before=$(docker logs "$peer" 2>&1)
  output=$(fixture "$container" attempt "$role" "$label") || status=$?
  echo "$output"
  [[ $status == 3 && $output == *"refused label=$label reason=$reason" && $output != *" dial "* ]]
  [[ $(docker inspect -f '{{.State.Health.Status}}' "$container") != healthy ]]
  events=$(docker logs "$peer" 2>&1)
  [[ $events == "$before" && $events != *"request label=$label"* ]]
}

worker_snapshot() {
  local container=$1 role=$2 pid peer id service
  docker inspect -f 'status={{.State.Status}} pid={{.State.Pid}} exit={{.State.ExitCode}} health={{.State.Health.Status}} failures={{.State.Health.FailingStreak}}{{range .State.Health.Log}}{{println}}healthcheck end={{.End}} exit={{.ExitCode}}{{end}}' "$container" || true
  docker top "$container" -eo pid,ppid,stat,comm || true
  pid=$(docker inspect -f '{{.State.Pid}}' "$container") || pid=0
  if [[ $pid != 0 ]]; then
    nsenter -t "$pid" -n ip -br addr || true
    nsenter -t "$pid" -n ip -4 route show table all || true
    nsenter -t "$pid" -n ip -6 route show table all || true
    nsenter -t "$pid" -n ss -tuan || true
    nsenter -t "$pid" -n nft list ruleset || true
    timeout 8s docker exec "$container" python /spikes/topology_fixture.py diagnose "$role" || true
  fi
  peer=check-target
  if [[ $role == notifications ]]; then peer=provider-target; fi
  for service in "worker-$role" "$peer" rabbitmq postgres; do
    id=$("${compose[@]}" ps -a -q "$service") || continue
    if [[ -n $id ]]; then
      echo "Diagnostics logs service=$service generation=$id"
      safe_logs "$id" || true
    fi
  done
}

wait_healthy() {
  local container=$1 role=$2 deadline=$((SECONDS+35)) observed reason
  while true; do
    if ! observed=$(docker inspect -f '{{.State.Status}} {{.State.Health.Status}}' "$container"); then
      reason=inspect-failed
      break
    fi
    if [[ $observed == 'running healthy' ]]; then return 0; fi
    if [[ $observed != running\ * ]]; then
      reason=container-not-running
      break
    fi
    if (( SECONDS >= deadline )); then
      reason=healthcheck-deadline
      break
    fi
    sleep 0.2
  done
  echo "Worker readiness failed role=$role generation=$container expected='running healthy (Celery ready file and live pidfile process)' observed='${observed:-unavailable}' reason=$reason" >&2
  worker_snapshot "$container" "$role"
  return 1
}

expect_policy_failure() {
  local status=0
  policy "$1" "$2" "$3" ip007-compose-v1 300 || status=$?
  [[ $status == 4 ]]
}

quarantine_counters() {
  local counter
  for counter in held_ipv4 held_ipv6; do
    nft list counter bridge "$table" "$counter" | grep -E 'packets [1-9][0-9]*'
    nft reset counter bridge "$table" "$counter" >/dev/null
  done
}

start_worker checks checks
start_worker notifications notifications
fixture "$checks" held checks
fixture "$notifications" held notifications
quarantine_counters
expect_policy_failure "$checks" checks initial
refuse "$checks" checks startup-missing missing-policy
refuse "$notifications" notifications provider-missing missing-policy
worker_rules "$checks" checks
worker_rules "$notifications" notifications
pid=$(docker inspect -f '{{.State.Pid}}' "$checks")
nsenter -t "$pid" -n nft add counter inet ip007_worker drift
expect_policy_failure "$checks" checks initial
refuse "$checks" checks startup-rule-drift missing-policy
nsenter -t "$pid" -n nft delete counter inet ip007_worker drift
policy "$checks" checks initial obsolete 300
refuse "$checks" checks startup-wrong-version stale-policy
policy "$notifications" notifications initial ip007-compose-v1 -1
refuse "$notifications" notifications provider-expired stale-policy
policy "$checks" checks initial ip007-compose-v1 300
policy "$notifications" notifications initial ip007-compose-v1 300
wire_gate delete 51 10
wire_gate delete 52 11
wait_healthy "$checks" checks
wait_healthy "$notifications" notifications
prepare_publication_probe
timeout 25s stdbuf -oL nft monitor trace > "$IP007_LAB/publication.trace" 2>&1 &
trace_pid=$!
verify_worker_gateway "$checks"
verify_publication 4
verify_publication 6
stop_publication_trace
publication_snapshot
fixture "$checks" coverage checks
fixture "$notifications" coverage notifications
for container in "$checks" "$notifications"; do
  pid=$(docker inspect -f '{{.State.Pid}}' "$container")
  for counter in always_deny default_deny dns dns_reply; do
    nsenter -t "$pid" -n nft list counter inet ip007_worker "$counter" |
      grep -E 'packets [1-9][0-9]*'
  done
done

identity() {
  sed 's/^.*) //' "/proc/$1/stat" 2>/dev/null | awk '{print $20}'
}

old=$checks
fixture "$old" send old-generation
wait_log "$target" 'request label=old-generation'
pid=$(docker inspect -f '{{.State.Pid}}' "$old")
[[ $(docker inspect -f '{{.HostConfig.PidMode}}' "$old") == '' ]]
old_namespace=$(readlink "/proc/$pid/ns/pid")
cgroup=$(awk -F: '$1 == 0 {print $3}' "/proc/$pid/cgroup")
[[ $cgroup == *"$old"* ]]
cgroup="/sys/fs/cgroup$cgroup"
pids=()
births=()
owner=$(docker logs "$old" 2>&1 | sed -n 's/.*pid=\([0-9]*\).*locks label=old-generation .*/\1/p')
[[ -n $owner ]]
owner_found=0
cgroup_type=$(cat "$cgroup/cgroup.type")
echo "Previous cgroup $cgroup type=$cgroup_type"
grep -Fx 'populated 1' "$cgroup/cgroup.events"
# cgroup.procs is unavailable in a threaded cgroup. Snapshot process
# leaders from cgroup.threads and use cgroup.events for the entire subtree.
threads=$(cat "$cgroup/cgroup.threads")
[[ -n $threads ]]
while read -r process; do
  if ! read -r leader local_pid < <(awk '
    /^Tgid:/ { leader = $2 }
    /^NSpid:/ { print leader, $NF }
  ' "/proc/$process/status") || [[ $process != "$leader" ]]; then
    continue
  fi
  if ! birth=$(identity "$process") || ! pidns=$(readlink "/proc/$process/ns/pid"); then
    # A transient Docker health check can exit while the snapshot is read.
    continue
  fi
  [[ -n $birth && $pidns == "$old_namespace" ]]
  pids+=("$process")
  births+=("$birth")
  if [[ $local_pid == "$owner" ]]; then owner_found=1; fi
  echo "Previous process generation=$old pidns=$old_namespace pid=$process nspid=$local_pid start=$birth"
done <<< "$threads"
(( ${#pids[@]} >= 4 && owner_found ))
old_locks=$(docker logs "$old" 2>&1 | sed -n 's/.*locks label=old-generation \(execution=[0-9:]* start=[0-9:]*\).*/\1/p')
[[ -n $old_locks ]]
api=$("${compose[@]}" ps -q api)
api_locks=$(docker exec "$api" python -c '
import os
from pathlib import Path
for kind in ("execution", "start"):
    path, = Path("/locks").glob(f"739ef7c5-0193-4c7d-8da8-de5067e27c6c.{kind}")
    stat = os.stat(path)
    print(f"{kind}={stat.st_dev}:{stat.st_ino}", end=" " if kind == "execution" else "\n")
')
[[ $api_locks == "$old_locks" ]]
docker kill --signal KILL "$old" >/dev/null
[[ $(docker wait "$old") == 137 ]]
[[ $(docker inspect -f '{{.State.Status}} {{.State.Pid}}' "$old") == 'exited 0' ]]
generation_gone() {
  local index current
  if [[ -d $cgroup ]]; then
    grep -Fxq 'populated 0' "$cgroup/cgroup.events" || return 1
    cgroup_state='populated 0'
  else
    cgroup_state=removed
  fi
  for index in "${!pids[@]}"; do
    current=$(identity "${pids[index]}") || current=
    [[ $current != "${births[index]}" ]] || return 1
  done
}
deadline=$((SECONDS+5))
until generation_gone; do
  if (( SECONDS >= deadline )); then
    echo "Previous generation still has live process identities: $old" >&2
    exit 1
  fi
  sleep 0.05
done
wait_log "$target" 'close peer=.* label=old-generation$'
safe_logs "$old"
echo "Previous cgroup $cgroup state=$cgroup_state"
echo "Confirmed stop of exact generation=$old pidns=$old_namespace and ${#pids[@]} processes"

wire_gate add 51 10
start_worker checks checks
[[ $checks != "$old" ]]
fixture "$checks" held checks
quarantine_counters
refuse "$checks" checks replacement-stale stale-policy
mv "$IP007_LAB/admission/checks.json" "$IP007_LAB/replaced-policy.json"
refuse "$checks" checks replacement-missing missing-policy
worker_rules "$checks" checks
policy "$checks" checks "$old" ip007-compose-v1 300
refuse "$checks" checks replacement-unconfirmed unconfirmed-generation
printf '%s\n' "$checks" > "$IP007_LAB/admission/stopped"
refuse "$checks" checks replacement-wrong-proof unconfirmed-generation
wire_gate delete 51 10
printf '%s\n' "$old" > "$IP007_LAB/admission/staged"
mv "$IP007_LAB/admission/staged" "$IP007_LAB/admission/stopped"
echo "Released proof generation=$old for successor=$checks"
wait_healthy "$checks" checks
fixture "$checks" send new-generation
wait_log "$target" 'request label=new-generation'
wait_log "$checks" 'completed label=new-generation'
new_locks=$(docker logs "$checks" 2>&1 | sed -n 's/.*locks label=new-generation \(execution=[0-9:]* start=[0-9:]*\).*/\1/p')
[[ $new_locks == "$old_locks" ]]
echo "Shared lock identity preserved: $new_locks"
fixture "$checks" coverage checks
verify_worker_gateway "$checks"
