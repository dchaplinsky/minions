"""
Django settings for minions project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_env_str(k, default):
    return os.environ.get(k, default)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_str('SECRET_KEY', 'iif2=3*v^#fh!x%t^%a^wsi%*d-+d9hi8g5nl##u#=2*au2z%i')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django_jinja',
    'django_jinja.contrib._easy_thumbnails',
    'easy_thumbnails',
    'core',
    'raven.contrib.django.raven_compat',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'minions.urls'

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

WSGI_APPLICATION = 'minions.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_str('DB_NAME', None),
        'USER': get_env_str('DB_USER', None),
        'PASSWORD': get_env_str('DB_PASS', None),
        'HOST': get_env_str('DB_HOST', None),
        'PORT': get_env_str('DB_PORT', 5432)
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'uk'
TIME_ZONE = 'Europe/Kiev'

USE_I18N = False
USE_L10N = False
USE_TZ = False

# Setup Elasticsearch default connection
ELASTICSEARCH_CONNECTIONS = {
    'default': {
        'hosts': 'localhost',
        'timeout': 20
    }
}

STATIC_URL = '/static/'
MEDIA_ROOT = get_env_str('MEDIA_ROOT', os.path.join(BASE_DIR, "media"))
STATIC_ROOT = get_env_str('STATIC_ROOT', os.path.join(BASE_DIR, "static"))
MEDIA_URL = '/media/'

from django_jinja.builtins import DEFAULT_EXTENSIONS

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": ".jinja",
            "context_processors": (
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ),
            "extensions": DEFAULT_EXTENSIONS + [
                "jinja2.ext.do",
                "jinja2.ext.loopcontrols",
                "jinja2.ext.with_",
                "jinja2.ext.i18n",
                "jinja2.ext.autoescape",
                "django_jinja.builtins.extensions.CsrfExtension",
                "django_jinja.builtins.extensions.CacheExtension",
                "django_jinja.builtins.extensions.TimezoneExtension",
                "django_jinja.builtins.extensions.UrlsExtension",
                "django_jinja.builtins.extensions.StaticFilesExtension",
                "django_jinja.builtins.extensions.DjangoFiltersExtension"
            ]
        }
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "OPTIONS": {
            "context_processors": (
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            )
        },
        "APP_DIRS": True
    },
]

THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (179, 179), 'crop': ",0", 'upscale': True},
    },
}

import raven

try:
    GIT_VERSION = raven.fetch_git_sha(os.path.abspath(os.path.join(BASE_DIR, "..")))
except raven.exceptions.InvalidGitRepository:
    GIT_VERSION = "undef"
    pass

RAVEN_CONFIG = {
    'dsn': get_env_str('RAVEN_DSN', None),
    'release': get_env_str('VERSION', GIT_VERSION),
}

ELASTICSEARCH_CONNECTIONS = {
    'default': {
        'hosts': get_env_str('ELASTICSEARCH_DSN', 'localhost:9200'),
        'timeout': 20
    }
}

CATALOG_PER_PAGE = 10

try:
    from .local_settings import *
except ImportError:
    pass


# Init Elasticsearch connections
from elasticsearch_dsl import connections
connections.connections.configure(**ELASTICSEARCH_CONNECTIONS)
