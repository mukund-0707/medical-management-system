"""
Development-specific settings.
"""

from decouple import config
from .base import *  # noqa: F401, F403


# ─────────────────────────────────────────────
# Security
# ─────────────────────────────────────────────
SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-dev-key-change-in-production'
)

DEBUG = True

ALLOWED_HOSTS = ['*']


# ─────────────────────────────────────────────
# Database — SQLite (Development Only)
# Production mein PostgreSQL use karna hai.
# ─────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PostgreSQL config (future / production use):
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME', default='msms_db'),
#         'USER': config('DB_USER', default='postgres'),
#         'PASSWORD': config('DB_PASSWORD', default='postgres'),
#         'HOST': config('DB_HOST', default='localhost'),
#         'PORT': config('DB_PORT', default='5432'),
#     }
# }


# ─────────────────────────────────────────────
# CORS (for React frontend in dev)
# ─────────────────────────────────────────────
# CORS_ALLOW_ALL_ORIGINS = True  # Enable when cors-headers is installed
