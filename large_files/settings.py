from django.core.exceptions import ImproperlyConfigured
from pathlib import Path
import os
import json
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://47357c22e50142f29937c78132db01d9@o1002892.ingest.sentry.io/5979869",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

SETTINGS_DIR = Path(__file__).resolve().parent
BASE_DIR = Path(__file__).resolve().parent.parent

try:
    with open(os.path.join(SETTINGS_DIR, 'creds/config.json')) as f:
        configs = json.loads(f.read())
except:
    configs = None
    print("Couldn't Find config file")

def get_env_var(setting, configs=configs):
 try:
     val = configs[setting]
     if val == 'True':
         val = True
     elif val == 'False':
         val = False
     return val
 except KeyError:
     error_msg = "ImproperlyConfigured: Set {0} environment variable".format(setting)
     raise ImproperlyConfigured(error_msg)
 except Exception as e:
     print ("some unexpected error occurred!", e)
     
DB_CONFIG = get_env_var("DB")

SECRET_KEY = 'django-insecure-l68rx%$%scdm&uy^4k6#6v7j9h6-cnxbtw1fb^ak2f*=!i91t_'

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "postman.ishantdahiya.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_extensions',
    'upload',
    'home',
    'data'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'large_files.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'large_files.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", DB_CONFIG["ENGINE"]),
        "NAME": os.environ.get("SQL_DATABASE", DB_CONFIG["NAME"]),
        "USER": os.environ.get("SQL_USER", DB_CONFIG["USER"]),
        "PASSWORD": os.environ.get("SQL_PASSWORD", DB_CONFIG["PASSWORD"]),
        "HOST": os.environ.get("SQL_HOST", DB_CONFIG["HOST"]),
        "PORT": os.environ.get("SQL_PORT", DB_CONFIG["PORT"]),
    }
}

DB_URI_DEFAULT = f'postgresql://{os.environ.get("SQL_USER", DB_CONFIG["USER"])}:{os.environ.get("SQL_PASSWORD", DB_CONFIG["PASSWORD"])}@{os.environ.get("SQL_HOST", DB_CONFIG["HOST"])}:{os.environ.get("SQL_PORT", DB_CONFIG["PORT"])}/{os.environ.get("SQL_DATABASE", DB_CONFIG["NAME"])}'
print(DB_URI_DEFAULT)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'