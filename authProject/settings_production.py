from datetime import timedelta
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# Mantén la clave secreta usada en producción en secreto.
SECRET_KEY = 'ad008af5f3de0b60b5a2b4bd09b120f19bd788fc3534a9ed792212866e93105d5d7d8bb6547f154115055cab7a5a9d4844a5'

# Desactiva el modo de depuración en producción.
DEBUG = False
# Lista de nombres de host permitidos para tu aplicación.
ALLOWED_HOSTS = ['berna2023.pythonanywhere.com']

CORS_ALLOW_ALL_ORIGINS = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'rest_framework',
    'authApp',
    'corsheaders',
    'import_export',
    'multiselectfield',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',


]

ROOT_URLCONF = 'authProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'authProject.wsgi.application'


# configuracion bd MySQL

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'berna2023$db_dh2ocol',
        'USER': 'berna2023',
        'PASSWORD': 'Preciosa1481$',
        'HOST': 'berna2023.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'STRICT_ALL_TABLES',
        },
   }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'es-pe'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')



# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#################CONFIGURACIONES HECHAS POR MI #################################################


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

}


# Configuración de archivos multimedia
MEDIA_URL = '/media/' # Define la URL base para acceder a los archivos multimedia
MEDIA_ROOT = os.path.join(BASE_DIR, 'authApp/media') # Define la ruta donde se guardarán los archivos multimedia cargados por los usuarios

# Security settings
# Establece el tiempo de vida de la cookie de sesión en un valor seguro.
SESSION_COOKIE_SECURE = True
# Establece el tiempo de vida de la cookie CSRF en un valor seguro.
CSRF_COOKIE_SECURE = True
# Establece el tiempo de duración de HSTS (HTTP Strict Transport Security) en segundos.
SECURE_HSTS_SECONDS = 3600  # Set an appropriate value for HSTS
# Redirige todas las solicitudes HTTP a HTTPS.
SECURE_SSL_REDIRECT = True
# Define si se deben incluir todos los subdominios en la configuración de HSTS.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# Define si tu sitio debe ser pre-cargado en la lista de pre-carga del navegador.
SECURE_HSTS_PRELOAD = True

