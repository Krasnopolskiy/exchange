from datetime import timedelta
from pathlib import Path

import environ

env = environ.Env()

# Django
# ______________________________________________________________________________________________________________________

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="django-insecure-l877hlus+3(@==crfz0$+mc^+4hdu#%&z=8&v*9^s)j!")

DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=())

CORS_ALLOWED_ORIGINS = env.list("DJANGO_CORS_ALLOWED_ORIGINS", default=())

CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=())

INSTALLED_APPS = (
    # django
    "daphne",
    # installed
    "corsheaders",
    # apps
    "backend.stream",
    "backend.binance",
)

MIDDLEWARE = (
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
)

ROOT_URLCONF = "backend.urls"

TEMPLATES = (
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": (),
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": (
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ),
        },
    },
)

WSGI_APPLICATION = "backend.wsgi.application"

ASGI_APPLICATION = "backend.asgi.application"

# Logging
# ______________________________________________________________________________________________________________________

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "simple"},
    },
    "loggers": {
        "root": {"level": "INFO", "handlers": ["console"]},
    },
}

# Caches
# ----------------------------------------------------------------------------------------------------------------------

REDIS_HOST = env.str("REDIS_HOST", default="127.0.0.1")

REDIS_PORT = env.int("REDIS_PORT", default=6379)

CACHE_REDIS_DB = env.int("REDIS_DB", default=0)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{CACHE_REDIS_DB}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    },
}

# Localization
# ______________________________________________________________________________________________________________________

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

# Channels
# ______________________________________________________________________________________________________________________

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
            "capacity": 1000,
            "expiry": 5,
        },
    },
}

# Celery
# ----------------------------------------------------------------------------------------------------------------------

CELERY_REDIS_DB = env.int("CELERY_REDIS_DB", default=1)

CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{CELERY_REDIS_DB}"

CELERY_CACHE_BACKEND = "django-cache"

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Binance
# ----------------------------------------------------------------------------------------------------------------------

BINANCE_WS_URL = "wss://fstream.binance.com/stream"

BINANCE_LOG_FILE = BASE_DIR / "data" / "binance" / "log.jsonl"
