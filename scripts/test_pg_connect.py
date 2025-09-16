import locale
import os
import sys
import traceback

POSTGRES_CONFIG = {
    "NAME": os.environ.get(
        "POSTGRES_DB", os.environ.get("NEUROCARE_DB_NAME", "postgres")
    ),
    "USER": os.environ.get(
        "POSTGRES_USER", os.environ.get("NEUROCARE_DB_USER", "postgres")
    ),
    "PASSWORD": os.environ.get(
        "POSTGRES_PASSWORD", os.environ.get("NEUROCARE_DB_PASSWORD", "postgres")
    ),
    "HOST": os.environ.get(
        "POSTGRES_HOST", os.environ.get("NEUROCARE_DB_HOST", "localhost")
    ),
    "PORT": os.environ.get(
        "POSTGRES_PORT", os.environ.get("NEUROCARE_DB_PORT", "5432")
    ),
}


def main():
    print("Python:", sys.version)
    print("Default encoding:", sys.getdefaultencoding())
    print("Filesystem encoding:", sys.getfilesystemencoding())
    print("Locale:", locale.getpreferredencoding())
    try:
        import psycopg2

        print("psycopg2 version:", psycopg2.__version__)
        conn = psycopg2.connect(
            dbname=POSTGRES_CONFIG["NAME"],
            user=POSTGRES_CONFIG["USER"],
            password=POSTGRES_CONFIG["PASSWORD"],
            host=POSTGRES_CONFIG["HOST"],
            port=POSTGRES_CONFIG["PORT"],
        )
        print("Connected OK")
        conn.close()
    except Exception:
        print("Connection failed, traceback:")
        traceback.print_exc()


if __name__ == "__main__":
    main()
