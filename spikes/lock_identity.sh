#!/usr/bin/env bash
set -euo pipefail
trace=$(mktemp)
holder=
cleanup() {
  if [[ -n $holder ]]; then
    wait "$holder" || true
  fi
  rm -f "$trace"
}
trap cleanup EXIT
id=$(python3 -c 'import uuid; print(uuid.uuid4())')
docker compose exec -T worker-checks python - hold "$id" < spikes/lock_identity.py > "$trace" &
holder=$!
deadline=$((SECONDS+5))
until [[ -s $trace ]]; do
  if (( SECONDS >= deadline )); then
    echo "Check worker did not confirm lock acquisition" >&2
    exit 1
  fi
  sleep 0.1
done
api=$(docker compose exec -T api python - busy "$id" < spikes/lock_identity.py)
[[ $api == "$(cat "$trace")" ]]
wait "$holder"
holder=
unlocked=$(docker compose exec -T api python - available "$id" < spikes/lock_identity.py)
[[ $unlocked == "${api% held} available" ]]
printf 'Forked worker and API shared lock inode %s, and reuse after exit succeeded\n' "${api% held}"
