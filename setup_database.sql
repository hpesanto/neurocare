-- ============================================================================
-- NeuroCare Database Setup Script
-- ============================================================================
-- This script creates the 'neurocare' schema in PostgreSQL.
-- 
-- Usage:
--   psql -U postgres -h localhost -c "CREATE DATABASE neurocare" 2>/dev/null || true
--   psql -U postgres -h localhost -d neurocare -f setup_database.sql
--
-- After this, run Django migrations:
--   python manage.py migrate
-- ============================================================================

-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS neurocare;

-- Grant permissions to postgres user
GRANT ALL PRIVILEGES ON SCHEMA neurocare TO postgres;

-- Set search_path to neurocare for all future objects in this database
ALTER DATABASE neurocare SET search_path TO neurocare, public;

-- Display confirmation
SELECT 'Schema neurocare created/verified successfully!' AS message;
