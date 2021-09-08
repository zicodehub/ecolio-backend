"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-zh^9@om#3udjv@6k33r4d*n@_h+8a^j4)0ow^!^#wwp)n4!!_a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
GLOBAL_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CONTRIB APPS
    'corsheaders',
    'rest_framework',
    'durin',
    'django_filters',

]

# Ces applications NE SERONT PAS  migrées dans les bases de données client
PRIVATE_APPS = [
    'core',
]

INSTALLED_APPS = [
    *GLOBAL_APPS,
    *PRIVATE_APPS,

    # APPS FOR EACH CLIENT
    'app_api',
    'app_auth',


]

# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',

#     # CUSTOM MIDDLEWARES
#     'core.middleware.ClientDatabaseRouterMiddleware',

# ]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # CUSTOM MIDDLEWARES
    'core.middleware.ClientDatabaseRouterMiddleware',

]

# CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS=['localhost', '127.0.0.1']
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]



# CORS_ALLOW_HEADERS = [
#     "x-code",
    
# ]
ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'server.wsgi.application'




################ DATABASES #############################################################################
""" 
            DATABASES
    Si la connection --default-- n'est pas définie et que l'application --core-- est installée,
    il doit TOUJOURS y avoir une base de donnée active en plus de la --default--
    Cela est dû à la fonction --create_database() de --core.utils qui utilise leur curseur

    Si la SUPER_USER_DATABASE et la DB du GATEWAY sont les mêmes, 
    il faudra quand même définir les 2 avec les mêmes configurations 



    SUPER_USER_DATABASE est obligatoire si l'application --core est installée
    Il est recommandé que ce soit une sqlite3 car est beaucoup sollicitée
    et n'est censée dépasser le million de lignes
"""

# SUPER_USER_DATABASE = {
#     'alias': 'SUPER_USER_DB', 
#     'conf': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'tir',
#         'USER': 'postgres',
#         'PASSWORD': 'root',
#         'HOST': 'localhost',
#         'PORT': ''
#     },
# }

SUPER_USER_DATABASE = {
    'alias': 'SUPER_USER_DB', 
    # 'conf': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'cfsgejkx',
    #     'USER': 'cfsgejkx',
    #     'PASSWORD': 'Y5JrtpAxob0FUnzxzmA62M82qzyG38fj',
    #     'HOST': 'chunee.db.elephantsql.com',
    #     'PORT': ''
    # },
    'conf': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tir',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': ''
    },
}

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'chouchou.sqlite3'
    },


	# 'gateway': {
 #        'ENGINE': 'django.db.backends.postgresql',
 #        'NAME': 'kfogrrvg',
 #        'USER': 'kfogrrvg',
 #        'PASSWORD': 'Dy7ZKa3Hh9mbud5Jcge4bf5-HwbpD8e_',
 #        'HOST': 'lallah.db.elephantsql.com',
 #        'PORT': ''
 #    },

    'gateway': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gateway',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': ''
    },
    
    SUPER_USER_DATABASE["alias"] : SUPER_USER_DATABASE["conf"]
   
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


############ REST_FRAMEWORK CONFIGURATIONS #######################################################

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': ('durin.auth.TokenAuthentication',),

    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    
    'FILTERS_DEFAULT_LOOKUP_EXPR' : 'icontains',

    
}

from datetime import timedelta
from rest_framework.settings import api_settings
REST_DURIN = {
        "DEFAULT_TOKEN_TTL": timedelta(days=1),
        "TOKEN_CHARACTER_LENGTH": 64,
        "USER_SERIALIZER": None,
        "AUTH_HEADER_PREFIX": "Token",
        "EXPIRY_DATETIME_FORMAT": api_settings.DATETIME_FORMAT,
        "TOKEN_CACHE_TIMEOUT": 60,
        "REFRESH_TOKEN_ON_LOGIN": True,
        "AUTHTOKEN_SELECT_RELATED_LIST": ["user"],
}


################## CORE APP CONFIGURATIONS ###########################################################

"""
    DATABASE_HEADER_ROUTER_NAME représente le champ du header des requêtes HTTP, 
    utilisé par l'application --core  pour router la requête dans la  bonne base de données
"""
DATABASE_HEADER_ROUTER_NAME = "X-Code"
DATABASE_LOGIN_ROUTER_NAME = "code"

""" 
    Utilisé par get_db_alias_from_request() de core.utils
    Un client durant tout le traitement d'une requete, les opérations en DB
    sont routées grace à une variable définie dans le thread de la requete.

    DATABASE_ALIAS_NAME_FROM_REQUEST indique le nom de cette variable
"""
DATABASE_ALIAS_NAME_FROM_REQUEST = 'db-alias'

""" 
    Model/Table de routage des requetes HTTP
"""
DATABASE_ROUTER_MODEL = "core.ClientDB"

##  ATTENTION, L'ORDRE EST TRES IMPORTANT
DATABASE_ROUTERS = [
    # Routeur static
    'core.routers.GatewayRouter',    

    # Au runtime, il gère les école
    'core.routers.RuntimeRouter',  

    # Pour l'entreprise manager de Ecolioo  
    'core.routers.TIRRouter',    
]
