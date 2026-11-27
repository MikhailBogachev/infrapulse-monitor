\set ON_ERROR_STOP on
CREATE TABLE IF NOT EXISTS ip007_guard (
  id uuid PRIMARY KEY,
  attempt integer NOT NULL,
  lease timestamptz NOT NULL
);
GRANT SELECT, INSERT, UPDATE, DELETE ON ip007_guard TO infrapulse_app;
ALTER TABLE ip007_guard ADD COLUMN IF NOT EXISTS paused boolean NOT NULL DEFAULT false;

CREATE TABLE IF NOT EXISTS ip007_guard_run (
  id uuid PRIMARY KEY,
  token integer NOT NULL DEFAULT 0,
  paused boolean NOT NULL DEFAULT false,
  active_job text,
  lease timestamptz,
  owner_pid integer,
  incarnation text,
  generation text
);
CREATE TABLE IF NOT EXISTS ip007_guard_result (
  id uuid REFERENCES ip007_guard_run ON DELETE CASCADE,
  job text,
  token integer NOT NULL,
  status integer NOT NULL,
  PRIMARY KEY (id, job)
);
CREATE TABLE IF NOT EXISTS ip007_guard_retired (
  id uuid REFERENCES ip007_guard_run ON DELETE CASCADE,
  job text,
  PRIMARY KEY (id, job)
);
GRANT SELECT, INSERT, UPDATE, DELETE ON
  ip007_guard_run, ip007_guard_result, ip007_guard_retired TO infrapulse_app;
