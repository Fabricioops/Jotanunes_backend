from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# DEV
DEBUG = True
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-secret')
ALLOWED_HOSTS = ['*']  # em produção, troque por domínio(s)

INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd-party
    'rest_framework',
    'corsheaders',
    'drf_spectacular',

    # Apps do projeto
    'core',
    'customizacoes',
    'users',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',                 # pode ficar no topo
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # <- precisa vir ANTES do AuthenticationMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],           # usamos templates dentro dos apps
        'APP_DIRS': True,     # <— importante p/ admin e templates dos apps
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

# --------- BANCO (SQL Server) ---------
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'importacao',
        'USER': '',  # deixa vazio
        'PASSWORD': '',  # deixa vazio
        'HOST': 'localhost',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'trusted_connection': 'yes',  # importante para Windows Authentication config do meu BD (fabricio)
        },
    }
}



LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Maceio'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'customizacoes' / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --------- DRF / JWT / Swagger ---------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=4),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Jota Nunes – API de Customizações',
    'DESCRIPTION': 'Gestão de customizações TOTVS (alertas, histórico, dependências).',
    'VERSION': '1.0.0',
}

# CORS (dev)
CORS_ALLOW_ALL_ORIGINS = True
