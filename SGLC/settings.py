# Django settings for SGLC project.
import os
try:
    from .local_settings import DEBUG
except Exception:
    DEBUG = True
# DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    ('Mauricio Aizaga', 'maizaga@daiech.com'),
    ('Edwin Mesa', 'emesa@daiech.com'),
    # ('Catalina Aristizabal', 'cataristi2002@hotmail.com'),
)

try:
    from .local_settings import URL_BASE, PROJECT_NAME, PROJECT_DESCRIPTION
except ImportError:
    URL_BASE = "http://destaju.com"
    PROJECT_NAME = "DESTAJU AGRO"
    PROJECT_DESCRIPTION = "Sistema Gestor de Labores de Campo"

APPS = ["apps.website", "apps.account", "apps.actions_log", "apps.emailmodule", "apps.pdfmodule",
"apps.process_admin", "apps.production_orders", "apps.payroll", 'django.contrib.humanize', 'south', 'apps.inventory' ]

EDITABLES_MODEL = {
                    "process_admin": ["Activities", "UserProfile"],
                    "auth": ["User"]
                }


try:
    import django_extensions
    APPS += ["django_extensions"]
except:
    pass

LOGIN_URL = "/cuenta/login"
LOGOUT_URL = "/cuenta/logout"
LOGIN_REDIRECT_URL = "/"
FROM_EMAIL = PROJECT_NAME + " <no-reply@daiech.com>"

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

try:
    from .local_settings import EMAIL_HOST_USER
except:
    EMAIL_HOST_USER = ""
try:
    from .local_settings import EMAIL_HOST_PASSWORD
except:
    EMAIL_HOST_PASSWORD = ""

MANAGERS = ADMINS

try:
    from .local_settings import DATABASES
except Exception, e:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3','NAME': 'db.sqlite','USER': '','PASSWORD': '','HOST': '','PORT': '',}}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["162.243.207.189", "destaju.mauricioaizaga.com"]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Bogota'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es'

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
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.sep.join([os.path.dirname(os.path.dirname(__file__)), 'public/media'])

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/home/dev/.statics/demo-destaju'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.sep.join([os.path.dirname(os.path.dirname(__file__)), 'public/static']),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'j95hbk+e&u2gutqfa7mmppvkac_l_mkc0q1b6*xiax*n)=giyu'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'SGLC.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'SGLC.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.sep.join([os.path.dirname(os.path.dirname(__file__)), 'templates']),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
) + tuple(APPS)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
    'apps.website.context_processors.get_project_name',
    'apps.website.context_processors.is_debug',
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
