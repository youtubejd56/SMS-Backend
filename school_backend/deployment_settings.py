import os
import dj_database_url
from .settings import *

# Debug should be off in deployment
DEBUG = False

# Host & CSRF settings from Render
ALLOWED_HOSTS = [os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")]
CSRF_TRUSTED_ORIGINS = [
    "https://" + os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
]

# Secret key from Render env
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", SECRET_KEY)

# Middleware (no duplicates)
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Storage (keeps same as base, but ensures whitenoise is used)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Database from DATABASE_URL
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
    )
}
