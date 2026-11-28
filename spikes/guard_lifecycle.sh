#!/usr/bin/env bash
# Run against a disposable Compose project. Docker control remains on the host.
set -euo pipefail
compose=("$@")
observer=
old=
new=
cleanup() {
  local status=$?
  trap - EXIT
  if (( status != 0 )); then
    if [[ -n $old && -z $new ]]; then docker logs "$old" || true; fi
    if [[ -n $new ]]; then docker logs "$new" || true; fi
    if [[ -n $observer ]]; then docker logs "$observer" || true; fi
  fi
  if [[ -n $observer ]]; then docker rm -f "$observer" >/dev/null; fi
  "${compose[@]}" rm -sf guard-worker >/dev/null
  exit "$status"
}
trap cleanup EXIT

"${compose[@]}" up -d --no-deps --force-recreate --wait --wait-timeout 25 guard-worker
old=$("${compose[@]}" ps -q guard-worker)
[[ -z $(docker inspect -f '{{.HostConfig.PidMode}}' "$old") ]]
observer=$("${compose[@]}" run -d --no-deps -T spike \
  pytest -q -s -p no:cacheprovider /spikes/test_celery_guard.py)
deadline=$((SECONDS+85))
until generation=$(docker exec "$observer" cat /tmp/guard-replace 2>/dev/null); do
  [[ $(docker inspect -f '{{.State.Running}}' "$observer") == true ]]
  (( SECONDS < deadline ))
  sleep 0.2
done

docker kill --signal KILL "$old" >/dev/null
[[ $(docker wait "$old") == 137 ]]
[[ $(docker inspect -f '{{.State.Status}} {{.State.Pid}}' "$old") == "exited 0" ]]
docker logs "$old"
"${compose[@]}" up -d --no-deps --force-recreate --wait --wait-timeout 25 guard-worker
new=$("${compose[@]}" ps -q guard-worker)
[[ -n $new && $new != "$old" ]]
printf 'Docker confirmed old container %.12s exited; replacement %.12s is ready\n' "$old" "$new"
docker exec "$observer" sh -ec 'printf "%s" "$1" > /tmp/guard-proof; mv /tmp/guard-proof /tmp/guard-recreated' sh "$generation"

deadline=$((SECONDS+35))
until [[ $(docker inspect -f '{{.State.Running}}' "$observer") == false ]]; do
  (( SECONDS < deadline ))
  sleep 0.2
done
docker logs "$observer"
[[ $(docker wait "$observer") == 0 ]]
docker stop --time 20 "$new" >/dev/null
[[ $(docker wait "$new") == 0 ]]
[[ $(docker inspect -f '{{.State.Status}} {{.State.Pid}}' "$new") == "exited 0" ]]
echo "Replacement worker stopped cleanly after settlement"
