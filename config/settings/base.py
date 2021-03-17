"""
Django settings for Boats & Joy project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import environ

BASE_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
APPS_DIR = BASE_DIR.path('boatsandjoy_api')

env = environ.Env()
environ.Env.read_env('.env')

# APP CONFIGURATION
# ******************************************************************************

# DEBUG
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', False)

# SECRET CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# ------------------------------------------------------------------------------
SECRET_KEY = env('DJANGO_SECRET_KEY')

INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Boats & Joy apps
    'boatsandjoy_api.core',
    'boatsandjoy_api.boats',
    'boatsandjoy_api.availability',
    'boatsandjoy_api.bookings',
    # Others
    'rest_framework',
    'corsheaders',
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',
]

# DATABASE CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB', default=''),
        'USER': env('POSTGRES_USER', default=''),
        'PASSWORD': env('POSTGRES_PASSWORD', default=''),
        'HOST': env('POSTGRES_HOST', default='localhost'),
        'PORT': env('POSTGRES_PORT', default='5432'),
        'CONN_MAX_AGE': env.int('DATABASE_CONN_MAX_AGE', default=300),
    }
}

# ADMIN CONFIGURATION
# ------------------------------------------------------------------------------
ADMIN_URL = 'admin/'

# URL CONFIGURATION
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# WSGI CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
# ------------------------------------------------------------------------------
WSGI_APPLICATION = 'config.wsgi.application'

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/Madrid'

# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en'
LANGUAGES = (('en', 'English'),)

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

DATE_FORMAT = '%Y-%m-%d'

# MIDDLEWARE CONFIGURATION
# https://docs.djangoproject.com/en/dev/topics/http/middleware/
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------
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

# TEMPLATE CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# STATIC FILES CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
# ------------------------------------------------------------------------------
STATIC_ROOT = str(BASE_DIR('staticfiles'))

# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (str(APPS_DIR.path('static')),)

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# THIRD PARTY APPLICATIONS
# ******************************************************************************

# Cors
# https://github.com/adamchainz/django-cors-headers
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = True

# Stripe
# https://github.com/stripe/stripe-python
# ------------------------------------------------------------------------------
STRIPE_API_KEY = env('STRIPE_API_KEY', default='')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY', default='')
STRIPE_ENDPOINT_SECRET = env('STRIPE_ENDPOINT_SECRET', default='')
STRIPE_REDIRECT_URL = env('STRIPE_REDIRECT_URL', default='')

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
