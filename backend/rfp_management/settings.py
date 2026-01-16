"""
Django settings for rfp_management project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-test-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0,testserver').split(',')

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'rest_framework',
    'corsheaders',
    'rfp_management.apps.vendors',
    'rfp_management.apps.rfps',
    'rfp_management.apps.proposals',
    'rfp_management.apps.ai',
    'rfp_management.apps.email_service',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rfp_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'rfp_management.wsgi.application'

# Database Configuration - Using SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['rest_framework.filters.SearchFilter'],
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
    'http://localhost:3000',
    'http://127.0.0.1:4200',
    'https://bookish-telegram-9rr4qpgpr9rcx7r-4200.app.github.dev',
]

# Email Configuration
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'rfp-system@example.com')

# IMAP Configuration
IMAP_SERVER = os.getenv('IMAP_SERVER', 'imap.gmail.com')
IMAP_PORT = int(os.getenv('IMAP_PORT', '993'))
IMAP_USERNAME = os.getenv('IMAP_USERNAME', '')
IMAP_PASSWORD = os.getenv('IMAP_PASSWORD', '')

# Ollama Configuration
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'tinyllama')

# Email Processing
EMAIL_CHECK_INTERVAL = int(os.getenv('EMAIL_CHECK_INTERVAL', '300'))
