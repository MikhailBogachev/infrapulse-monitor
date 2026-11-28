#!/usr/bin/env bash
# Sourced by topology.sh. All links, namespaces and rules belong to this run.

probe_ns="$COMPOSE_PROJECT_NAME"
probe_link="ip7-${table:6:10}"
probe_v4=198.18.7.2
probe_v6=fd42:213:53::2
# Use distinct source ports across address families so a completed control
# cannot leave a dual-stack bind or TIME_WAIT collision for the other family.
control_ports=([4]=38180 [6]=38182)
denied_ports=([4]=38181 [6]=38183)
trace_pid=
probe_namespace=0
listener_rules=0

host_policy() {
  local family ip worker gateway target source tuple probe_tuple control_port denied_port
  {
    cat <<RULES
table inet $table {
  counter host_v4 {}
  counter host_v6 {}
  counter worker_input_v4 {}
  counter worker_input_v6 {}
  counter worker_dnat_v4 {}
  counter worker_dnat_v6 {}
  counter ingress_v4 {}
  counter ingress_v6 {}
  counter published_v4 {}
  counter published_v6 {}
  counter control_v4 {}
  counter control_v6 {}
  chain before_dnat {
    type filter hook prerouting priority -110; policy accept;
RULES
    for family in 4 6; do
      read -r ip worker gateway target source < <(publication_addresses "$family")
      control_port=${control_ports[$family]}
      denied_port=${denied_ports[$family]}
      cat <<RULES
    iifname "ip007-check" $ip saddr $worker $ip daddr $gateway tcp dport { 18080, 18081 } tcp flags & (syn | ack) == syn meta nftrace set 1
    iifname "$probe_link" $ip saddr $source $ip daddr $gateway tcp sport { $control_port, $denied_port } tcp dport 18080 tcp flags & (syn | ack) == syn meta nftrace set 1
    iifname "$probe_link" $ip saddr $source $ip daddr $gateway tcp sport $denied_port tcp dport 18080 counter name ingress_v$family
RULES
    done
    cat <<RULES
  }
  chain input {
    type filter hook input priority -5; policy accept;
    iifname "ip007-check" ip daddr 10.213.51.1 tcp dport 18081 counter name host_v4 drop
    iifname "ip007-check" ip6 daddr fd42:213:51::1 tcp dport 18081 counter name host_v6 drop
    iifname "ip007-check" ip saddr 10.213.51.10 ip daddr 10.213.51.1 tcp dport 18080 counter name worker_input_v4 drop
    iifname "ip007-check" ip6 saddr fd42:213:51::10 ip6 daddr fd42:213:51::1 tcp dport 18080 counter name worker_input_v6 drop
    iifname { "ip007-control", "ip007-check", "ip007-provider", "$probe_link" } meta l4proto tcp drop
  }
  chain forward {
    type filter hook forward priority -5; policy accept;
RULES
    for family in 4 6; do
      read -r ip worker gateway target source < <(publication_addresses "$family")
      control_port=${control_ports[$family]}
      denied_port=${denied_ports[$family]}
      tuple="ct direction original ct status dnat ct original $ip daddr $gateway ct original proto-dst 18080 ct reply $ip saddr $target ct reply proto-src 8080"
      probe_tuple="$tuple ct original $ip saddr $source ct reply $ip daddr $source"
      cat <<RULES
    iifname "ip007-check" $ip saddr $worker $ip daddr $target tcp dport 8080 $tuple counter name worker_dnat_v$family drop
    iifname "$probe_link" $ip saddr $source $ip daddr $target tcp sport $denied_port tcp dport 8080 $probe_tuple ct original proto-src $denied_port ct reply proto-dst $denied_port counter name published_v$family drop
    iifname "$probe_link" $ip saddr $source $ip daddr $target tcp sport $control_port tcp dport 8080 $probe_tuple ct original proto-src $control_port ct reply proto-dst $control_port counter name control_v$family accept
RULES
    done
    cat <<RULES
    iifname "$probe_link" drop
    oifname "$probe_link" ct status dnat ct direction reply accept
    oifname "$probe_link" drop
    iifname "ip007-check" oifname != "ip007-check" drop
    iifname "ip007-provider" oifname != "ip007-provider" drop
  }
}
RULES
  } | apply
}

publication_addresses() {
  if [[ $1 == 4 ]]; then
    printf '%s\n' "ip 10.213.51.10 10.213.51.1 $nginx_v4 $probe_v4"
  else
    printf '%s\n' "ip6 fd42:213:51::10 fd42:213:51::1 $nginx_v6 $probe_v6"
  fi
}

prepare_publication_probe() {
  ip netns add "$probe_ns"
  probe_namespace=1
  ip link add "$probe_link" type veth peer name eth0 netns "$probe_ns"
  ip addr add 198.18.7.1/30 dev "$probe_link"
  ip -6 addr add fd42:213:53::1/64 dev "$probe_link" nodad
  ip link set "$probe_link" up
  ip -n "$probe_ns" link set lo up
  ip -n "$probe_ns" link set eth0 up
  ip -n "$probe_ns" addr add "$probe_v4/30" dev eth0
  ip -n "$probe_ns" -6 addr add "$probe_v6/64" dev eth0 nodad
  ip -n "$probe_ns" route add 10.213.51.1/32 via 198.18.7.1
  ip -n "$probe_ns" -6 route add fd42:213:51::1/128 via fd42:213:53::1

  # Observe SYN delivery before the Nginx socket, including any connection that
  # reaches it without sending an HTTP request.
  apply nsenter -t "$nginx_pid" -n <<RULES
table inet $table {
  counter received_v4 {}
  counter received_v6 {}
  chain input {
    type filter hook input priority -5; policy accept;
    ip saddr $probe_v4 ip daddr $nginx_v4 tcp sport { ${control_ports[4]}, ${denied_ports[4]} } tcp dport 8080 tcp flags & (syn | ack) == syn counter name received_v4
    ip6 saddr $probe_v6 ip6 daddr $nginx_v6 tcp sport { ${control_ports[6]}, ${denied_ports[6]} } tcp dport 8080 tcp flags & (syn | ack) == syn counter name received_v6
  }
}
RULES
  listener_rules=1
}

counter_packets() {
  local counter=$1
  shift
  "$@" nft list counter inet "$table" "$counter" |
    awk '$1 == "packets" && $2 ~ /^[0-9]+$/ { count = $2; found++ }
         END { if (found != 1) exit 1; print count }'
}

check_counter_delta() {
  local expected=$1 counter=$2 before=$3 after
  shift 3
  after=$(counter_packets "$counter" "$@")
  echo "Packets counter=$counter before=$before after=$after expected=$expected"
  case "$expected" in
    increase) (( after > before ));;
    unchanged) (( after == before ));;
    *) return 2;;
  esac
}

verify_publication() {
  local family=$1 ip worker gateway target source url status=0 ingress published received control
  local control_port=${control_ports[$family]} denied_port=${denied_ports[$family]}
  local listener=(nsenter -t "$nginx_pid" -n)
  read -r ip worker gateway target source < <(publication_addresses "$family")
  url="http://$gateway:18080/health/live"
  if [[ $family == 6 ]]; then url="http://[$gateway]:18080/health/live"; fi
  received=$(counter_packets "received_v$family" "${listener[@]}")
  control=$(counter_packets "control_v$family")
  ip netns exec "$probe_ns" curl "-$family" --noproxy '*' -fsS --max-time 3 \
    --local-port "$control_port" "$url"
  check_counter_delta increase "control_v$family" "$control"
  check_counter_delta increase "received_v$family" "$received" "${listener[@]}"
  # Dropped SYNs can have unconfirmed conntrack tuples. The named FORWARD
  # counters match both tuples inline while the entry still exists.
  conntrack -L -f "ipv$family" -p tcp --orig-src "$source" --orig-dst "$gateway" \
    --sport "$control_port" --dport 18080

  ingress=$(counter_packets "ingress_v$family")
  published=$(counter_packets "published_v$family")
  received=$(counter_packets "received_v$family" "${listener[@]}")
  ip netns exec "$probe_ns" curl "-$family" --noproxy '*' -fsS --max-time 1 \
    --local-port "$denied_port" "$url" || status=$?
  echo "Published IPv$family ingress=$probe_link original=[$source]:$denied_port->[$gateway]:18080 translated=[$target]:8080 curl=$status"
  [[ $status == 28 ]] || return 1
  check_counter_delta increase "ingress_v$family" "$ingress"
  check_counter_delta increase "published_v$family" "$published"
  check_counter_delta unchanged "received_v$family" "$received" "${listener[@]}"
}

verify_worker_gateway() {
  local container=$1 family input_after dnat_after
  local -a input_before dnat_before host_before
  for family in 4 6; do
    input_before[$family]=$(counter_packets "worker_input_v$family")
    dnat_before[$family]=$(counter_packets "worker_dnat_v$family")
    host_before[$family]=$(counter_packets "host_v$family")
  done
  fixture "$container" gateway
  for family in 4 6; do
    input_after=$(counter_packets "worker_input_v$family")
    dnat_after=$(counter_packets "worker_dnat_v$family")
    echo "Worker IPv$family publication denial INPUT=${input_before[$family]}->$input_after FORWARD=${dnat_before[$family]}->$dnat_after"
    (( input_after > input_before[family] || dnat_after > dnat_before[family] ))
    check_counter_delta increase "host_v$family" "${host_before[$family]}"
  done
}

publication_snapshot() {
  local tool chain
  for tool in iptables ip6tables; do
    "$tool" -w 2 -t nat -S PREROUTING
    "$tool" -w 2 -t nat -nvxL DOCKER | awk '/ip007-check|18080/'
    for chain in FORWARD DOCKER-FORWARD DOCKER-ISOLATION-STAGE-1 DOCKER-ISOLATION-STAGE-2; do
      "$tool" -w 2 -S "$chain" 2>/dev/null || true
    done
  done
  ss -lntp '( sport = :18080 or sport = :18081 )'
  nsenter -t "$nginx_pid" -n ss -lnt '( sport = :8080 )'
}

stop_publication_trace() {
  if [[ -n $trace_pid ]]; then
    kill "$trace_pid" 2>/dev/null || true
    wait "$trace_pid" || true
    trace_pid=
    cat "$IP007_LAB/publication.trace"
  fi
}
