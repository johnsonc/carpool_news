"""
Django settings for carpool_news project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# openshift is our PAAS for now.
ON_PAAS = 'OPENSHIFT_REPO_DIR' in os.environ


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

if ON_PAAS:
    SECRET_KEY = os.environ['OPENSHIFT_SECRET_TOKEN']
else:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = ')j-sa8z)p%6-20kt%x&8v!wths_h&(m!2*9%h_ix7zwvpkk=fr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not ON_PAAS
DEBUG = DEBUG or 'DEBUG' in os.environ
if ON_PAAS and DEBUG:
    print("*** Warning - Debug mode is on ***")

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar.apps.DebugToolbarConfig',
    'bootstrap3',
    'rides',
    'users',
)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Django debug toolbar
INTERNAL_IPS = (
    '127.0.0.1',
)

ROOT_URLCONF = 'carpool_news.urls'

WSGI_APPLICATION = 'carpool_news.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if ON_PAAS:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME':     os.environ['OPENSHIFT_APP_NAME'],
            'USER':     os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
            'PASSWORD': os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
            'HOST':     os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
            'PORT':     os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
        }
    }
else:
    # Local Postgres instance for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': 'localhost',
            'PORT': '',
            'NAME': 'carpool_news',
            'USER': 'carpool_news',
            'PASSWORD': 'carpool_news',
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'wsgi', 'static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Templates
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)

LOGIN_URL = '/users/login'

# Application settings
NEWEST_RIDES = 10
RIDES_PER_PAGE = 10

# django-bootstrap3 settings
BOOTSTRAP3 = {
    'horizontal_label_class': 'col-md-3',
    'horizontal_field_class': 'col-md-9',
    # Do not add 'has-success' class on sucessfully submitted forms
    'success_css_class': '',
}

# Mailgun configuration
MAIL_API_URL = 'https://api.mailgun.net/v2/sandboxf55c93f91bc9469b9b5e1817832f1ee7.mailgun.org/messages'
MAIL_API_KEY = 'key-ace37b47312c34bad12f63cb1cdc468d'
MAIL_FROM = 'Carpool News <mailer@carpoolnews-tomasra.rhcloud.com>'
MAIL_SUBJECT = 'Nauji skelbimai'
