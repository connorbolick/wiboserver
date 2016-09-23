import os, locale
from decimal import Decimal

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
ALLOWED_HOSTS = ['*']
TEMPLATE_DEBUG = True

ADMINS = [
    # ("Your Name", "your_email@example.com"),
]

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        #"NAME": os.path.join(PACKAGE_ROOT,'../..','dev.db'),
	#"NAME": "database_name",
	"NAME": "wibo",
	#"HOST": "localhost",
	"HOST": "/tmp/mysql.sock",
	"PORT": "3306",
	"USER": "wiboAdmin",
	"PASSWORD": "CUbanners16!",
	}
}
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "US/Eastern"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

#-Set the locale setting. This is used for localization
# of stuff like currency formatting. Probably overkill, but still...-
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/site_media/static/"

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PACKAGE_ROOT, "static"),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
]

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    #"pinax_utils.context_processors.settings",
    "pinax_theme_bootstrap.context_processors.theme",
    "account.context_processors.account",
]


MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "wibo.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "wibo.wsgi.application"

TEMPLATE_DIRS = [
    os.path.join(PACKAGE_ROOT, "templates"),
    #os.path.join(SETTINGS_PATH, ),
]

INSTALLED_APPS = [
    "grappelli",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    #"django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    
    # theme
    "pinax_theme_bootstrap_account",
    "pinax_theme_bootstrap",
    "django_forms_bootstrap",
    "bootstrapform",    

    # external
    "account",
    "metron",
    "eventlog",
    
    # batch importing
    "csvimport",

    # search
    #"haystack",
    "django_select2",

    # database
#    "south",
    
    # project
    "wibo",
    "contacts",
    "cards",
    "inventory",
    "invoice",
    "employee",
    "roi",
    "reports",
    "timetask",
]


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    }
}

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ACCOUNT_OPEN_SIGNUP = False
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2

AUTHENTICATION_BACKENDS = [
    "account.auth_backends.UsernameAuthenticationBackend",
]

# should be moved into a table for global settins
TAX_RATE = Decimal(0.07)
WAGE_RATE = Decimal(7.25)
# divide the width and height (in inches)
# to get the number of feet
# (change to 100 if using metric units)
IN_PER_FT = 12
# rush fee defaults
R12_MIN = Decimal(15)
R12_PER = Decimal(.15)
R24_MIN = Decimal(10)
R24_PER = Decimal(.10)
R48_MIN = Decimal(5)
R48_PER = Decimal(.05)
# for new Employee accounts
DEFAULT_PASSWORD = 'design'
# for ink cost (in USD) per unit (sqft for large format, each for small)
ROLAND_INK = Decimal(0.35)
HP_INK = Decimal(0.22)
DIGITAL_INK = Decimal(0.08)
# settings for grappelli (admin)
GRAPPELLI_ADMIN_TITLE = "WIBO - Admin Panel"

# debug_toolbar settings
if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INSTALLED_APPS += (
        'debug_toolbar',
    )

    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        #'debug_toolbar.panels.profiling.ProfilingDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.cache.CacheDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
    )

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

# haystack search settings
# HAYSTACK_SITECONF = 'search_sites'
# HAYSTACK_SEARCH_ENGINE = 'whoosh'
# HAYSTACK_WHOOSH_PATH = os.path.join(os.path.dirname(__file__), 'whoosh_index')

try:
    from local_settings import *
except ImportError:
    pass
