from pathlib import Path
import os
from dotenv import load_dotenv

# Load .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# -----------------------------
# Basic secrets / flags
# -----------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "insecure-dev-key")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Use DJANGO_DEBUG env var (set to '0' or '1' or 'true'/'false')
DJANGO_DEBUG = os.getenv("DJANGO_DEBUG")
if DJANGO_DEBUG is None:
    DEBUG = True
else:
    DEBUG = DJANGO_DEBUG in ("1", "True", "true", "yes", "YES")

# ALLOWED_HOSTS from env (comma separated). Defaults to localhost in DEBUG.
_allowed = os.getenv("ALLOWED_HOSTS", "")
if _allowed:
    ALLOWED_HOSTS = [h.strip() for h in _allowed.split(",") if h.strip()]
else:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"] if DEBUG else []

# -----------------------------
# Installed apps
# -----------------------------
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    # Local apps
    'attendance_app',
]

# If CLOUDINARY_URL is provided, enable cloudinary apps for media storage
if os.getenv("CLOUDINARY_URL"):
    INSTALLED_APPS += ["cloudinary", "cloudinary_storage"]

# -----------------------------
# Middleware
# -----------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -----------------------------
# CORS / CSRF
# -----------------------------
CORS_ALLOWED_ORIGINS = [o.strip() for o in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()]
if DEBUG and not CORS_ALLOWED_ORIGINS:
    # development default for Vite/React dev server
    CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]

CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]

# -----------------------------
# REST framework
# -----------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
 
}

# -----------------------------
# Static & Media
# -----------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ✅ Point to React build static (no more warnings)
STATICFILES_DIRS = [
    BASE_DIR / 'frontend' / 'build' / 'static',
]

# Use WhiteNoise for static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media handling: prefer Cloudinary when CLOUDINARY_URL is set (recommended on Render)
if os.getenv("CLOUDINARY_URL"):
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# -----------------------------
# Templates
# -----------------------------
ROOT_URLCONF = 'school_backend.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', BASE_DIR / 'frontend' / 'build'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'school_backend.wsgi.application'

# -----------------------------
# Database (use DATABASE_URL on Render or local MySQL fallback)
# -----------------------------
DATABASE_URL = os.getenv('DATABASE_URL')

DEFAULT_DB = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': os.getenv('MYSQL_DATABASE', 'school_db'),
    'USER': os.getenv('MYSQL_USER', 'root'),
    'PASSWORD': os.getenv('MYSQL_PASSWORD', ''),
    'HOST': os.getenv('MYSQL_HOST', '127.0.0.1'),
    'PORT': os.getenv('MYSQL_PORT', '3306'),
    'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'"
    }
}

if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
    except Exception:
        DATABASES = {'default': DEFAULT_DB}
else:
    DATABASES = {'default': DEFAULT_DB}

# -----------------------------
# Password validation
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

# -----------------------------
# Internationalization
# -----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# -----------------------------
# Security when DEBUG=False
# -----------------------------
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', 3600))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True').lower() in ('1', 'true', 'yes')
    SECURE_HSTS_PRELOAD = os.getenv('SECURE_HSTS_PRELOAD', 'True').lower() in ('1', 'true', 'yes')

# -----------------------------
# Misc
# -----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

