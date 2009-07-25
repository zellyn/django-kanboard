DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/tmp/kanboard.db'
INSTALLED_APPS = ['kanboard']
ROOT_URLCONF = ['kanboard.urls']

DEBUG=True

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.auth',

    'kanboard',
)

ROOT_URLCONF = 'kanboard.testurls'
