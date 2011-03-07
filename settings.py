# Django settings for optools project.

import os

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Vincent BESANCON', 'vincent.besancon@faurecia.com'),
)

MANAGERS = (
	('Mohamed CHERROUD', 'mohamed.cherroud-ext@faurecia.com'),
)

DATABASES = {
	'default': {
        'ENGINE': 'django.db.backends.mysql', 		# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'optools',							# Or path to database file if using sqlite3.
        'USER': 'optools',                      				# Not used with sqlite3.
        'PASSWORD': '62SBU3pNJnVVBA5D',                  				# Not used with sqlite3.
        'HOST': 'localhost',                      				# Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      				# Set to empty string for default. Not used with sqlite3.
    },
    'test': {
        'ENGINE': 'django.db.backends.sqlite3', 		# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_PATH, 'db/master.db'),							# Or path to database file if using sqlite3.
        'USER': '',                      				# Not used with sqlite3.
        'PASSWORD': '',                  				# Not used with sqlite3.
        'HOST': '',                      				# Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      				# Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/django/optools/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5w=ojm+vgosx4au22-=+zbfa@e((67*%m#%mv!tumnawm98+s6'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

# List of template context processors
TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.request',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.contrib.messages.context_processors.messages',
	'django.contrib.auth.context_processors.auth',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'optools.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    
    # Reporting
	'optools.apps.reporting',
	
	# Nagios
	'optools.apps.nagios',
	
	# Highlights
	'optools.apps.highlights',
)
