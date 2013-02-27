# Django settings for example project.
import os

#The Production setting allows apps and links to be turned on and off
#To set PRODUCTION = False, set PRODUCTION = False in your copy of credentials.py
#Don't change the value here since this file is shared between many deployments
PRODUCTION = True

from credentials import *

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(ROOT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/media/'

STATIC_ROOT = os.path.join(ROOT_PATH, 'sitestatic')
STATIC_URL = '/static/'
STATIC_DOC_ROOT = os.path.join(ROOT_PATH, 'static')
STATICFILES_DIRS = (STATIC_DOC_ROOT,)

#ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'physics_django.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH, 'templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    #django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    #django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    #django.contrib.messages.context_processors.messages"
    "apps.user_interface.context_processors.is_production"
)


INSTALLED_APPS_PROD = (
    'django.contrib.staticfiles', # include static files
    #'magnets',                 # Component type editor
)

# Apps should be added here until they are ready to deploy in production
INSTALLED_APPS_DEV = (

    'magnets',

    #Third party apps
    'crispy_forms',
    'extra_views',
)

if PRODUCTION:
    INSTALLED_APPS = INSTALLED_APPS_PROD
else:
    INSTALLED_APPS = INSTALLED_APPS_PROD + INSTALLED_APPS_DEV

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=apps',
    # '--cover-inclusive'
]


