"""
Django settings for wikilegis project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

from decouple import config, Csv
from django.utils.translation import ugettext_lazy as _
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# APPLICATION SETTINGS
DEBUG = config('DEBUG', cast=bool, default=True)

SECRET_KEY = config('SECRET_KEY', default='secret_key')

SITE_ID = config('SITE_ID', default='1')

ALLOWED_HOSTS = config('ALLOWED_HOSTS',
                       cast=Csv(lambda x: x.strip().strip(',').strip()),
                       default='*')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'compressor',
    'compressor_toolkit',
    'django_extensions',
    'rest_framework',
    'django_filters',
    'django_js_reverse',
    'constance',
    'constance.backends.database',

    'apps.accounts',
    'apps.participations',
    'apps.projects',
    'apps.notifications',
    'apps.api',
    'apps.dashboard',
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

ROOT_URLCONF = 'wikilegis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wikilegis.processors.settings_variables',
            ],
        },
    },
]

WSGI_APPLICATION = 'wikilegis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.' + config('DATABASE_ENGINE',
                                                 default='sqlite3'),
        'NAME': config('DATABASE_NAME',
                       default=os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': config('DATABASE_USER', default=''),
        'PASSWORD': config('DATABASE_PASSWORD', default=''),
        'HOST': config('DATABASE_HOST', default=''),
        'PORT': config('DATABASE_PORT', default=''),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGES = (
    ('en', 'English'),
    ('pt-br', 'Brazilian Portuguese'),
)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

LANGUAGE_CODE = config('LANGUAGE_CODE', default='pt-br')

TIME_ZONE = config('TIME_ZONE', default='America/Sao_Paulo')

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = config('STATIC_URL', default='/static/')
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'public', 'static'))

MEDIA_URL = config('MEDIA_URL', default='/media/')
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'public', 'media'))

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'npm.finders.NpmFinder',
    'compressor.finders.CompressorFinder',
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

NPM_ROOT_PATH = os.path.dirname(BASE_DIR)
COMPRESS_OFFILNE = config('COMPRESS_OFFILNE', default=not DEBUG, cast=bool)

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'compressor_toolkit.precompilers.SCSSCompiler'),
)

NODE_MODULES = os.path.join(NPM_ROOT_PATH, 'node_modules')
COMPRESS_NODE_MODULES = NODE_MODULES
COMPRESS_NODE_SASS_BIN = os.path.join(NODE_MODULES, '.bin/node-sass')
COMPRESS_POSTCSS_BIN = os.path.join(NODE_MODULES, '.bin/postcss')
COMPRESS_SCSS_COMPILER_CMD = '{node_sass_bin}' \
                             ' --source-map true' \
                             ' --source-map-embed true' \
                             ' --source-map-contents true' \
                             ' --output-style expanded' \
                             ' {paths} "{infile}" "{outfile}"' \
                             ' &&' \
                             ' {postcss_bin}' \
                             ' --use "{node_modules}/postcss-font-magician"' \
                             ' --use "{node_modules}/autoprefixer"' \
                             ' --autoprefixer.browsers' \
                             ' "{autoprefixer_browsers}"' \
                             ' -r "{outfile}"'

# EMAIL SETTINGS
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', cast=int, default=587)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='')
EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend'
)

# API
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'apps.api.permissions.ApiKeyPermission',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.'
                                'PageNumberPagination',
    'PAGE_SIZE': 20
}


if config('ENABLE_REMOTE_USER', default=0, cast=bool):
    AUTHENTICATION_BACKENDS = [
        'apps.accounts.backends.WikilegisAuthBackend',
    ]
    MIDDLEWARE.append('apps.accounts.middlewares.WikilegisRemoteUser')
else:
    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
    ]

FORCE_SCRIPT_NAME = config('FORCE_SCRIPT_NAME', default='')
SESSION_COOKIE_NAME = config('SESSION_COOKIE_NAME', default='sessionid')

CONSTANCE_CONFIG = {
    'USE_CD_OPEN_DATA': (
        True,
        _('Get document information from Câmara dos Deputados open data'),
        bool
    ),
    'CD_OPEN_DATA_URL': (
        'https://dadosabertos.camara.leg.br/api/v2/',
        _('Câmara dos Deputados open data API')
    ),
    'MIN_SUGGESTIONS': (
        50,
        _('Minimum suggestions to clustering')
    )
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
