# coding: UTF-8
# Django settings for new31 project.
import os

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))


DEBUG = False if 'SERVER_SOFTWARE' in os.environ else True

if DEBUG:
    # local
    MYSQL_DB = 'app_new31'
    MYSQL_USER = 'root'
    MYSQL_PASS = '123456'
    MYSQL_HOST_M = 'localhost'
    MYSQL_HOST_S = 'localhost'
    MYSQL_PORT = '3306'

else:
    # SAE
    import sae.const
    MYSQL_DB = sae.const.MYSQL_DB
    MYSQL_USER = sae.const.MYSQL_USER
    MYSQL_PASS = sae.const.MYSQL_PASS
    MYSQL_HOST_M = sae.const.MYSQL_HOST
    MYSQL_HOST_S = sae.const.MYSQL_HOST_S
    MYSQL_PORT = sae.const.MYSQL_PORT

    # 修改上传时文件在内存中可以存放的最大size为10m
    FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

    # sae的本地文件系统是只读的，修改django的file storage backend为Storage
    DEFAULT_FILE_STORAGE = 'sae.ext.django.storage.backend.Storage'

    # 使用media这个bucket
    STORAGE_BUCKET_NAME = 'media'
    # ref: https://docs.djangoproject.com/en/dev/topics/files/

    ALLOWED_HOSTS = ['*']


# DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('leiddx.ErEli', 'leiddx@vip.qq.com'),
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': MYSQL_DB,                      # Or path to database file if using sqlite3.
        'USER': MYSQL_USER,                      # Not used with sqlite3.
        'PASSWORD': MYSQL_PASS,                  # Not used with sqlite3.
        'HOST': MYSQL_HOST_M,                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': MYSQL_PORT,                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-CN'

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
MEDIA_ROOT = os.path.join(ROOT_PATH, 'media/').replace('\\','/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"

STATIC_ROOT = os.path.join(ROOT_PATH, 'static/').replace('\\','/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH, 'new31/static/').replace('\\','/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ytb#a#z=avwsbx@9)p*e_!r99b5k$@p0$38a36jid!cl6@05*k'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    # 'jinja2.jinja2_loader.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

ROOT_URLCONF = 'new31.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'new31.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH, 'new31/templates').replace('\\','/'),
)

APPS = {
    'shop':'',
    'account':'UserMiddleware',
    'purview':'purviewMiddleware',
    'cart':'CartMiddleware',
    'logistics':'CnsgnMiddleware',
    'order':'OrdMiddleware',
    'finance':'FncMiddleware',
    'item':'',
    'payment':'',
    'deliver':'',
    'signtime':'',
    'area':'',
    'tag':'',
    'message':'',
    'office':'',
    'spec':'',
    'discount':'',
    'produce':'',
    'inventory':'',
    'log':'',
    'upload':'',
    'print':'',
    'bom':'',
    'article':'',
    'wechat':'',
    'weight':'',
    'tasting':'',
    }


djangoMidClass = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'jinja2.middleware.tagMiddleware',
]

djangoTempContext = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
]

djangoAPPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    # 'south',
    # 'haystack',
]


for i,v in APPS.items():

    djangoAPPS.append(i)

    if v:
        djangoMidClass.append(u'%s.middleware.%s' % (i, v))

if not 'SERVER_SOFTWARE' in os.environ:
    djangoAPPS.append('debug_toolbar')
    djangoMidClass.append('debug_toolbar.middleware.DebugToolbarMiddleware')

    INTERNAL_IPS = ('127.0.0.1',)
    DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

INSTALLED_APPS = tuple(djangoAPPS)

MIDDLEWARE_CLASSES = tuple(djangoMidClass)

TEMPLATE_CONTEXT_PROCESSORS = tuple(djangoTempContext)

SESSION_COOKIE_AGE= 60 * 60 * 12
# SESSION_COOKIE_NAME = 'new31'
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_DOMAIN = 'www.31kecake.com'

# MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

LOGIN_URL = 'account:login'
LOGOUT_URL = 'account:logout'
LOGIN_REDIRECT_URL = 'account:myOrd'

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
        }
    }
}


HAYSTACK_CONNECTIONS = {
    'default': {
        # For Whoosh:
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
        # 'URL': 'http://localhost:9001/solr/example',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
    'whoosh': {
        # For Whoosh:
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        'INCLUDE_SPELLING': True,
    },
}