#!/usr/bin/env bash
set -euo pipefail
compose=(docker compose)
base_url=${INFRAPULSE_BASE_URL:-http://127.0.0.1:8080}
curl -fsS --max-time 5 "$base_url/health/live" | python3 -c 'import json, sys; assert json.load(sys.stdin) == {"status": "live"}'
curl -fsS --max-time 5 "$base_url/health/ready" | python3 -c 'import json, sys; assert json.load(sys.stdin) == {"status": "ready"}'
[[ $(curl -sS --max-time 5 -o /dev/null -w '%{http_code}' "$base_url/api/v1/unknown") == 404 ]]
ids=$("${compose[@]}" exec -T scheduler python -m infrapulse.smoke)
services=(worker-checks worker-notifications scheduler)
index=0
while IFS= read -r id; do
  [[ $id =~ ^[0-9a-f-]{36}$ ]]
  service=${services[$index]}
  until_time=$((SECONDS+15))
  until "${compose[@]}" logs --since 1m "$service" | grep -F '"event": "smoke_completed"' | grep -F "\"task_id\": \"$id\"" >/dev/null; do
    if (( SECONDS >= until_time )); then
      echo "Timed out waiting for smoke task $id on $service" >&2
      exit 1
    fi
    sleep 1
  done
  printf 'Database smoke task %s completed on %s\n' "$id" "$service"
  index=$((index+1))
done <<< "$ids"
[[ $index == 3 ]]
