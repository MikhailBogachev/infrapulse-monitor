\set ON_ERROR_STOP on
BEGIN;
CREATE SCHEMA ip007_ddl;
SET LOCAL search_path = ip007_ddl;
SET LOCAL timezone = 'UTC';

CREATE TABLE workspace (id uuid PRIMARY KEY);
CREATE TABLE monitor (
  id uuid PRIMARY KEY,
  workspace_id uuid NOT NULL REFERENCES workspace(id),
  target text,
  deleted_at timestamptz,
  UNIQUE (workspace_id, id)
);
CREATE TABLE schedule_epoch (
  workspace_id uuid NOT NULL,
  monitor_id uuid NOT NULL,
  id uuid NOT NULL,
  PRIMARY KEY (workspace_id, monitor_id, id),
  FOREIGN KEY (workspace_id, monitor_id) REFERENCES monitor(workspace_id, id)
);
CREATE TABLE check_execution (
  id uuid PRIMARY KEY,
  workspace_id uuid NOT NULL,
  monitor_id uuid NOT NULL,
  sequence bigint NOT NULL,
  epoch_id uuid,
  due_at timestamptz,
  completed_at timestamptz,
  status text NOT NULL,
  CHECK ((epoch_id IS NULL) = (due_at IS NULL)),
  FOREIGN KEY (workspace_id, monitor_id) REFERENCES monitor(workspace_id, id),
  FOREIGN KEY (workspace_id, monitor_id, epoch_id) REFERENCES schedule_epoch,
  UNIQUE (workspace_id, monitor_id, sequence),
  UNIQUE (workspace_id, monitor_id, epoch_id, due_at),
  UNIQUE (workspace_id, monitor_id, id, completed_at)
);
CREATE UNIQUE INDEX one_active_execution ON check_execution (workspace_id, monitor_id)
  WHERE status IN ('QUEUED', 'RUNNING');
CREATE TABLE check_result (
  completed_at timestamptz NOT NULL,
  execution_id uuid NOT NULL,
  workspace_id uuid NOT NULL,
  monitor_id uuid NOT NULL,
  PRIMARY KEY (completed_at, execution_id),
  FOREIGN KEY (workspace_id, monitor_id, execution_id, completed_at)
    REFERENCES check_execution (workspace_id, monitor_id, id, completed_at)
) PARTITION BY RANGE (completed_at);
CREATE INDEX history ON check_result (workspace_id, monitor_id, completed_at DESC, execution_id DESC);
CREATE TABLE results_00 PARTITION OF check_result
  FOR VALUES FROM ('2026-01-01 00:00+00') TO ('2026-01-01 06:00+00');
CREATE TABLE results_06 (LIKE check_result INCLUDING DEFAULTS);
ALTER TABLE check_result ATTACH PARTITION results_06
  FOR VALUES FROM ('2026-01-01 06:00+00') TO ('2026-01-01 12:00+00');
CREATE TABLE incident (
  id uuid PRIMARY KEY,
  workspace_id uuid NOT NULL,
  monitor_id uuid NOT NULL,
  execution_snapshot uuid,
  closed_at timestamptz,
  FOREIGN KEY (workspace_id, monitor_id) REFERENCES monitor(workspace_id,id)
);
CREATE UNIQUE INDEX one_open_incident ON incident (workspace_id, monitor_id) WHERE closed_at IS NULL;

CREATE FUNCTION fixture(i integer) RETURNS uuid LANGUAGE sql IMMUTABLE
  AS $$ SELECT lpad(i::text, 32, '0')::uuid $$;
CREATE FUNCTION expect_sqlstate(statement text, expected text) RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  EXECUTE statement;
  RAISE EXCEPTION 'Expected SQLSTATE %: %', expected, statement;
EXCEPTION WHEN others THEN
  IF SQLSTATE <> expected THEN RAISE; END IF;
END $$;

INSERT INTO workspace VALUES (fixture(1)), (fixture(2));
INSERT INTO monitor VALUES (fixture(3),fixture(1),'https://target.test');
INSERT INTO schedule_epoch VALUES (fixture(1),fixture(3),fixture(4));
INSERT INTO check_execution VALUES
  (fixture(5),fixture(1),fixture(3),1,fixture(4),'2026-01-01 05:55','2026-01-01 05:59','DONE'),
  (fixture(6),fixture(1),fixture(3),2,NULL,NULL,'2026-01-01 06:00','DONE'),
  (fixture(7),fixture(1),fixture(3),3,NULL,NULL,NULL,'RUNNING'),
  (fixture(8),fixture(1),fixture(3),4,NULL,NULL,'2026-01-01 12:00','DONE');
INSERT INTO check_result VALUES
  ('2026-01-01 05:59',fixture(5),fixture(1),fixture(3)),
  ('2026-01-01 06:00',fixture(6),fixture(1),fixture(3));
INSERT INTO incident VALUES (fixture(9),fixture(1),fixture(3),fixture(5));

SELECT expect_sqlstate('ALTER TABLE check_result ADD UNIQUE (execution_id)', '0A000');
SELECT expect_sqlstate('INSERT INTO check_result SELECT * FROM check_result', '23505');
SELECT expect_sqlstate(
  $$INSERT INTO check_result VALUES ('2026-01-01 06:01',fixture(5),fixture(1),fixture(3))$$,
  '23503');
DELETE FROM check_result WHERE execution_id = fixture(5);
SELECT expect_sqlstate(
  $$INSERT INTO check_result VALUES ('2026-01-01 05:59',fixture(5),fixture(2),fixture(3))$$,
  '23503');
INSERT INTO check_result VALUES ('2026-01-01 05:59',fixture(5),fixture(1),fixture(3));
SELECT expect_sqlstate(
  $$INSERT INTO check_result VALUES ('2026-01-01 12:00',fixture(8),fixture(1),fixture(3))$$,
  '23514');
SELECT expect_sqlstate(
  $$INSERT INTO check_execution VALUES
    (fixture(10),fixture(1),fixture(3),5,NULL,NULL,NULL,'QUEUED')$$, '23505');
SELECT expect_sqlstate(
  $$INSERT INTO check_execution VALUES
    (fixture(10),fixture(1),fixture(3),5,fixture(4),'2026-01-01 05:55',NULL,'DONE')$$,
  '23505');
SELECT expect_sqlstate(
  $$INSERT INTO check_execution VALUES
    (fixture(10),fixture(1),fixture(3),2,NULL,NULL,NULL,'DONE')$$, '23505');
SELECT expect_sqlstate('DELETE FROM check_execution WHERE id = fixture(5)', '23503');
SELECT expect_sqlstate('DELETE FROM monitor WHERE id = fixture(3)', '23503');

SET LOCAL plan_cache_mode = force_generic_plan;
PREPARE recent(timestamptz, timestamptz) AS
  SELECT * FROM check_result WHERE completed_at >= $1 AND completed_at < $2
    AND workspace_id = fixture(1) AND monitor_id = fixture(3);
DO $$
DECLARE line text;
DECLARE pruned boolean := false;
BEGIN
  FOR line IN EXECUTE
    $plan$EXPLAIN (ANALYZE, COSTS OFF) EXECUTE recent('2026-01-01 06:00','2026-01-01 12:00')$plan$
  LOOP
    RAISE NOTICE '%', line;
    pruned := pruned OR line LIKE '%Subplans Removed: 1%';
  END LOOP;
  IF NOT pruned THEN RAISE EXCEPTION 'Prepared execution did not prune the expired partition'; END IF;
END $$;

DO $$
BEGIN
  IF (SELECT count(*) FROM check_result
      WHERE completed_at > '2026-01-31 05:59+00'::timestamptz - interval '30 days'
        AND completed_at <= '2026-01-31 05:59+00') <> 1
  THEN RAISE EXCEPTION 'Retention cutoff mismatch'; END IF;
END $$;
SET LOCAL lock_timeout = '1s';
ALTER TABLE check_result DETACH PARTITION results_00;
DROP TABLE results_00;
DELETE FROM check_execution WHERE id = fixture(5);
UPDATE monitor SET target = NULL, deleted_at = now() WHERE id = fixture(3);
UPDATE incident SET closed_at = now() WHERE monitor_id = fixture(3);
DELETE FROM check_result WHERE monitor_id = fixture(3);
DELETE FROM check_execution WHERE monitor_id = fixture(3);
DELETE FROM schedule_epoch WHERE monitor_id = fixture(3);

DO $$
BEGIN
  IF EXISTS (SELECT FROM check_result) OR EXISTS (SELECT FROM check_execution)
     OR (SELECT count(*) FROM incident WHERE execution_snapshot = fixture(5)
         AND closed_at IS NOT NULL) <> 1
     OR NOT EXISTS (SELECT FROM monitor WHERE target IS NULL AND deleted_at IS NOT NULL)
  THEN RAISE EXCEPTION 'Deletion or incident retention mismatch'; END IF;
END $$;
ROLLBACK;
\echo PostgreSQL DDL, partition and incident checks passed
