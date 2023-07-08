from .settings import *

# import dj_database_url

DEBUG = config("DEBUG", False, cast = bool)

SECRET_KEY = config('SECRET_KEY', SECRET_KEY)

ALLOWED_HOSTS = ["warrenintel.com", "symplyfinance.co", "symplyfinance.up.railway.app"]

CSRF_TRUSTED_ORIGINS = ["https://" + host for host in ALLOWED_HOSTS]

# DATABASES = {
#     'default': dj_database_url.config(
#         conn_max_age=600,
#         conn_health_checks=True,
#     ),
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':  config('PGDATABASE'),
        'USER': config('PGUSER'),
        'PASSWORD': config('PGPASSWORD'),
        'HOST': config('PGHOST'),
        'PORT': config('PGPORT'),
    }
}



STORAGES = {
    "staticfiles":{
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"
    }
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

INSTALLED_APPS.append("treblle")
INSTALLED_APPS.remove("debug_toolbar")

MIDDLEWARE.append("treblle.middleware.TreblleMiddleware")
MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")

