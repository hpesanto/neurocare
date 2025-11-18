#!/usr/bin/env python3
"""
NeuroCare Database Setup Script
================================
This script sets up a PostgreSQL database and applies Django migrations.

Requirements:
- PostgreSQL installed and running
- psycopg2 installed (included in requirements.txt)
- Django configured in settings.py

Usage:
    python setup_postgres.py

Or with custom connection parameters:
    NEUROCARE_DB_HOST=myhost NEUROCARE_DB_USER=myuser python setup_postgres.py
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Get database configuration from environment
DB_HOST = os.getenv("NEUROCARE_DB_HOST") or os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("NEUROCARE_DB_PORT") or os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("NEUROCARE_DB_NAME") or os.getenv("POSTGRES_DB", "neurocare")
DB_USER = os.getenv("NEUROCARE_DB_USER") or os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("NEUROCARE_DB_PASSWORD") or os.getenv("POSTGRES_PASSWORD", "postgres")

SCHEMA_NAME = "neurocare"


def connect_to_postgres(db_name="postgres"):
    """Connect to PostgreSQL with given database name."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=db_name,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        conn.autocommit = True
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        sys.exit(1)


def create_database():
    """Create the neurocare database if it doesn't exist."""
    print(f"📦 Creating database '{DB_NAME}'...")
    
    conn = connect_to_postgres("postgres")
    cursor = conn.cursor()
    
    try:
        # Check if database exists
        cursor.execute(
            f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'"
        )
        if cursor.fetchone():
            print(f"   ✓ Database '{DB_NAME}' already exists")
        else:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(DB_NAME)
            ))
            print(f"   ✓ Database '{DB_NAME}' created")
    finally:
        cursor.close()
        conn.close()


def setup_schema():
    """Create the neurocare schema and set permissions."""
    print(f"🏗️  Setting up schema '{SCHEMA_NAME}'...")
    
    conn = connect_to_postgres(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Create schema
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}")
        print(f"   ✓ Schema '{SCHEMA_NAME}' created/verified")
        
        # Grant permissions
        cursor.execute(
            f"GRANT ALL PRIVILEGES ON SCHEMA {SCHEMA_NAME} TO {DB_USER}"
        )
        print(f"   ✓ Permissions granted to user '{DB_USER}'")
        
        # Set search_path
        cursor.execute(
            f"ALTER DATABASE {DB_NAME} SET search_path TO {SCHEMA_NAME}, public"
        )
        print(f"   ✓ Search path set to '{SCHEMA_NAME}'")
        
    finally:
        cursor.close()
        conn.close()


def run_django_migrations():
    """Run Django migrations to create tables."""
    print("🔧 Running Django migrations...")
    
    try:
        # Change to project directory
        os.chdir(BASE_DIR)
        
        # Run migrations
        result = subprocess.run(
            [sys.executable, "manage.py", "migrate"],
            capture_output=True,
            text=True,
        )
        
        if result.returncode == 0:
            print("   ✓ Migrations completed successfully")
            print(result.stdout)
        else:
            print("   ❌ Migration failed:")
            print(result.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"   ❌ Error running migrations: {e}")
        sys.exit(1)


def verify_setup():
    """Verify that tables were created."""
    print("✅ Verifying database setup...")
    
    conn = connect_to_postgres(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Count tables in neurocare schema
        cursor.execute(f"""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = '{SCHEMA_NAME}'
        """)
        table_count = cursor.fetchone()[0]
        
        # List tables
        cursor.execute(f"""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = '{SCHEMA_NAME}'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        print(f"\n   Database: {DB_NAME}")
        print(f"   Schema: {SCHEMA_NAME}")
        print(f"   Tables created: {table_count}")
        
        if tables:
            print("\n   Tables in schema:")
            for (table,) in tables:
                print(f"      - {table}")
        
        print("\n✨ Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ Verification failed: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def main():
    """Main setup flow."""
    print("=" * 70)
    print("NeuroCare PostgreSQL Database Setup")
    print("=" * 70)
    print(f"\nConfiguration:")
    print(f"  Host: {DB_HOST}")
    print(f"  Port: {DB_PORT}")
    print(f"  Database: {DB_NAME}")
    print(f"  User: {DB_USER}")
    print(f"  Schema: {SCHEMA_NAME}")
    print()
    
    try:
        create_database()
        setup_schema()
        run_django_migrations()
        
        if verify_setup():
            print("\n" + "=" * 70)
            print("✅ Setup completed! Your database is ready to use.")
            print("=" * 70)
            return 0
        else:
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
        return 1
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
