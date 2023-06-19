from datetime import timedelta
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

CORS_ALLOW_ALL_ORIGINS = True


# Application definition

BASE_APPS = [
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
]

LOCAL_APPS = [
    #'jazzmin',
    'rest_framework_simplejwt',
    'rest_framework',
    'drf_yasg',
    'authApp',
    'corsheaders',
    'import_export',
    'multiselectfield',
    
]

THIRD_APPS = [
    
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS


BASE_MIDDLEWARE = [
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

LOCAL_MIDDLEWARE = [
    
    'corsheaders.middleware.CorsMiddleware',
    
    
]

THIRD_MIDDLEWARE = [
    
]

MIDDLEWARE = BASE_MIDDLEWARE + LOCAL_MIDDLEWARE + THIRD_MIDDLEWARE


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


# MySQL para produccion
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'db_dh2ocol',
#        'USER': 'berna2023',
#        'PASSWORD': 'Mateo2023$',
#        'HOST': 'berna2023.mysql.pythonanywhere-services.com',
#        'PORT': '3306',
#   }
#}


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
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'authApp/static')
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#################CONFIGURACIONES HECHAS POR MI #################################################


JAZZMIN_SETTINGS = {
    'site_title': 'AppDh2oCol',
    'site_logo': 'img/logo v2.png',
    'site_header': 'Dh2oCol',
    'site_brand': "Dh2oColApp",
    'welcome_sign': 'Inicio de Sesion',
    "copyright": "Dh2oCol",
    "search_model": "auth.User",
    "show_sidebar": True,
    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index",
            "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues",
            "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "books"},
    ],

    'icons': {
        'auth.user': 'fas fa-user',
        'auth.Group': 'fas fa-users',

    }

}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "slate",
}

#CORS_ALLOWED_ORIGINS = [
#    "https://example.com",
#    "https://sub.example.com",
#    "http://localhost:8080",
#    "http://127.0.0.1:9000",
#] 

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

# Configuración de correo electrónico
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Ejemplo: 'smtp.gmail.com'
EMAIL_PORT = 587  # Ejemplo: 587
EMAIL_USE_TLS = True  # O False si no se requiere TLS
EMAIL_HOST_USER = 'dh2ovpar@gmail.com'
EMAIL_HOST_PASSWORD = 'tu_contraseña_de_correo_electronico'
DEFAULT_FROM_EMAIL = 'dh2ovpar@gmail.com'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'





