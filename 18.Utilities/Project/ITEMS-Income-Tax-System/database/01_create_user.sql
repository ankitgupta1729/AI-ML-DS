-- =============================================================================
-- ITEMS · Income Tax Evaluation & Maintenance System
-- 01_create_user.sql  —  create the application schema/user
--
-- Run as a privileged account (SYSTEM, or ADMIN on Oracle Autonomous DB).
--   sqlplus system/<pwd>@<service> @01_create_user.sql
-- On Oracle 12c+ multitenant, connect to the PDB first (ALTER SESSION SET
-- CONTAINER = <pdb>) or prefix the username with C## for a common user.
-- =============================================================================

-- Adjust the password to your environment / security policy.
CREATE USER ITEMS IDENTIFIED BY "Items#2025";

GRANT CREATE SESSION           TO ITEMS;
GRANT RESOURCE                 TO ITEMS;
GRANT CREATE TABLE             TO ITEMS;
GRANT CREATE VIEW              TO ITEMS;
GRANT CREATE SEQUENCE          TO ITEMS;
GRANT CREATE TRIGGER           TO ITEMS;
GRANT CREATE PROCEDURE         TO ITEMS;

-- Give the schema space to grow (skip on Autonomous DB — quota is automatic).
ALTER USER ITEMS QUOTA UNLIMITED ON USERS;

-- From here on, connect as the ITEMS user:
--   sqlplus ITEMS/"Items#2025"@<service>
-- and run 02_create_schema.sql, 03_seed_data.sql, 04_triggers_audit.sql.
