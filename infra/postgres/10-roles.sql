\set ON_ERROR_STOP on
\set migration_password `cat /run/secrets/infrapulse_migration_password`
\set app_password `cat /run/secrets/infrapulse_db_password`
BEGIN;
CREATE ROLE infrapulse_migrate LOGIN PASSWORD :'migration_password';
CREATE ROLE infrapulse_app LOGIN PASSWORD :'app_password';
REVOKE CONNECT, TEMPORARY ON DATABASE infrapulse FROM PUBLIC;
GRANT CONNECT ON DATABASE infrapulse TO infrapulse_migrate, infrapulse_app;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
GRANT CREATE, USAGE ON SCHEMA public TO infrapulse_migrate;
GRANT USAGE ON SCHEMA public TO infrapulse_app;
COMMIT;
