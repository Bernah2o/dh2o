from .base import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# configuracion bd postgres para desarrollo

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bd_dh2o',
        'USER': 'postgres',
        'PASSWORD': '15172967',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
