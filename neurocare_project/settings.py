import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
# Load project .env explicitly from the repository root so development variables
# (like NEUROCARE_DB_*) are available when running scripts or Django commands.
load_dotenv(BASE_DIR / ".env")

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

# Logging configuration to show SQL queries and debug messages from pacientes.views
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django.db.backends": {"handlers": ["console"], "level": "DEBUG"},
        "pacientes.views": {"handlers": ["console"], "level": "DEBUG"},
    },
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "pacientes",
    "profissionais",
    "evolucao_clinica",
    "avaliacao_neuropsicologica",
    "status_objetivo_reabilitacao",
    "formas_cobranca_reabilitacao",
    "reabilitacao_neuropsicologica",
    "reabilitacao_sessao",
    "vendas",
    "vendas_geral",
    "reabilitacao_objetivo",
    "transacoes",
    "tipos_transacao",
    "status_pagamento",
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

# DATABASE configuration: use PostgreSQL. Provide credentials via environment
# variables (or the .env file at project root). This forces Postgres as the
# database backend for development and production.
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
    "OPTIONS": {"options": "-c search_path=neurocare"},
}

# Force PostgreSQL as the project's database backend.
DATABASES = {"default": POSTGRES_CONFIG}


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
LOGIN_REDIRECT_URL = "/"
