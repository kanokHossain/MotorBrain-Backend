"""
Development settings for MotorBrain.
"""

from .base import *  # noqa: F401, F403

DEBUG = True

# Django Debug Toolbar (optional, install separately)
# INSTALLED_APPS += ["debug_toolbar"]
# MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
# INTERNAL_IPS = ["127.0.0.1"]

# Simplified email in development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
