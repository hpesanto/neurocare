import logging
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Security: read SECRET_KEY from environment in production. Keep a development fallback.
SECRET_KEY = os.environ.get("NEUROCARE_SECRET_KEY", "please-change-me-in-development")

# DEBUG should be False in production. Read from env to control environments.
DEBUG = os.environ.get("NEUROCARE_DEBUG", "true").lower() in ("1", "true", "yes")

ALLOWED_HOSTS = (
    os.environ.get("NEUROCARE_ALLOWED_HOSTS", "").split(",")
    if os.environ.get("NEUROCARE_ALLOWED_HOSTS")
    else []
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "pacientes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "neurocare_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "neurocare_project.context_processors.menu",
            ],
        },
    },
]

WSGI_APPLICATION = "neurocare_project.wsgi.application"
# DATABASE configuration: read Postgres settings from env. If not set or connection fails
# the application will fall back to sqlite for local development convenience.
POSTGRES_CONFIG = {
    "ENGINE": "django.db.backends.postgresql",
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


def _select_database():
    logger = logging.getLogger(__name__)
    try:
        import psycopg2

        # Try a lightweight connection to validate credentials/driver/encoding
        conn = psycopg2.connect(
            dbname=POSTGRES_CONFIG["NAME"],
            user=POSTGRES_CONFIG["USER"],
            password=POSTGRES_CONFIG["PASSWORD"],
            host=POSTGRES_CONFIG["HOST"],
            port=POSTGRES_CONFIG["PORT"],
        )
        conn.close()
        return {"default": POSTGRES_CONFIG}
    except UnicodeDecodeError as e:
        # Matches the traceback seen earlier: driver/encoding issue; fall back to sqlite
        logger.warning(
            "PostgreSQL connection failed due to encoding issue; falling back to sqlite3. Error: %s",
            e,
        )
    except Exception as e:
        # psycopg2 missing or other connection error — fall back to sqlite for development convenience.
        logger.warning(
            "PostgreSQL connection unavailable; falling back to sqlite3. Error: %s", e
        )

    return {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }


DATABASES = _select_database()


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "/"
