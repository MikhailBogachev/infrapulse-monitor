#!/bin/sh
# Runs inside the disposable Compose PostgreSQL container.
set -eu
psql_run() { psql -X -v ON_ERROR_STOP=1 -U infrapulse_admin -d infrapulse "$@"; }
suffix=$(psql_run -Atc "SELECT pg_backend_pid()")
case "$suffix" in *[!0-9]*|'') exit 2 ;; esac
fixture=ip007_locks_$suffix
reader=ip007_reader_$suffix
holder=
cleanup() {
  if [ -n "$holder" ]; then
    psql_run -Atc "SELECT pg_cancel_backend(pid) FROM pg_stat_activity WHERE application_name = '$reader'" >/dev/null
    wait "$holder" || true
  fi
  psql_run -qc "DROP SCHEMA $fixture CASCADE" >/dev/null
}
trap cleanup EXIT

psql_run -qc "
  CREATE SCHEMA $fixture;
  CREATE TABLE $fixture.history (completed_at timestamptz) PARTITION BY RANGE(completed_at);
  CREATE TABLE $fixture.expired PARTITION OF $fixture.history
    FOR VALUES FROM ('2026-01-01 00:00+00') TO ('2026-01-01 06:00+00');
  CREATE TABLE $fixture.fresh (LIKE $fixture.history);"

PGAPPNAME=$reader psql_run -qc "
  BEGIN;
  LOCK TABLE ONLY $fixture.history IN ACCESS SHARE MODE;
  SELECT pg_sleep(8);
  ROLLBACK;" >/dev/null 2>&1 &
holder=$!
tries=30
while [ "$(psql_run -Atc "
  SELECT count(*) FROM pg_locks l JOIN pg_stat_activity a USING (pid)
  WHERE a.application_name = '$reader'
    AND l.relation = '$fixture.history'::regclass AND l.granted")" -lt 1 ]; do
  tries=$((tries - 1))
  [ "$tries" -gt 0 ]
  sleep 0.1
done

psql_run -qc "
  SET lock_timeout = '300ms';
  ALTER TABLE $fixture.history ATTACH PARTITION $fixture.fresh
    FOR VALUES FROM ('2026-01-01 06:00+00') TO ('2026-01-01 12:00+00');"
if output=$(psql_run -v VERBOSITY=verbose -qc "
  SET lock_timeout = '300ms';
  ALTER TABLE $fixture.history DETACH PARTITION $fixture.expired;" 2>&1); then
  echo 'DETACH unexpectedly bypassed a concurrent reader' >&2
  exit 1
fi
printf '%s\n' "$output" | grep -F '55P03'
psql_run -Atc "SELECT pg_cancel_backend(pid) FROM pg_stat_activity WHERE application_name = '$reader'" >/dev/null
wait "$holder" || true
holder=
psql_run -qc "
  SET lock_timeout = '1s';
  ALTER TABLE $fixture.history DETACH PARTITION $fixture.expired;
  DROP TABLE $fixture.expired;"
echo 'ATTACH succeeded with a reader, DETACH timed out and succeeded after reader cancellation'
