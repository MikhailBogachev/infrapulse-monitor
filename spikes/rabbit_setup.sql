\set ON_ERROR_STOP on
CREATE TABLE IF NOT EXISTS ip007_effects (
  id uuid PRIMARY KEY,
  recorded_at timestamptz NOT NULL DEFAULT now()
);
GRANT SELECT, INSERT, DELETE ON ip007_effects TO infrapulse_app;
CREATE TABLE IF NOT EXISTS ip007_outbox (
  id uuid PRIMARY KEY,
  published boolean NOT NULL DEFAULT false
);
GRANT SELECT, INSERT, UPDATE, DELETE ON ip007_outbox TO infrapulse_app;
