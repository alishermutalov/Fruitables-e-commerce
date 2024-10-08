"""
Django settings for fruitables project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _
import dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv.load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+1q2ivf#e(*fs_33*zy2fb-w&u1qf3q7wt8d2ul!!7vpp%rz@4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



LANGUAGES = [
    ("uz", _("Uzbek")),
    ("en", _("English")),
    ("ru", _("Russian")),
]
MODELTRANSLATION_TRANSLATION_FILES = (
    'home.translation',
)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'

# Application definition



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Required for django-allauth
    #external apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'modeltranslation',
    #internal apps
    'home',
    'accounts',
    'payment',
    
]


STRIPE_PUBLIC_KEY =  os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_ENDPOINT_SECRET = os.getenv('STRIPE_ENDPOINT_SECRET')

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Required for default auth
    'allauth.account.auth_backends.AuthenticationBackend',  # Required for django-allauth
]
SITE_ID = 1
# settings.py

LOGIN_REDIRECT_URL = 'home'  # Redirect after successful login
LOGOUT_REDIRECT_URL = 'home'  # Redirect after logout
LOCALE_PATHS = BASE_DIR , 'locale' 

CSRF_TRUSTED_ORIGINS = [
    
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware', #allauth middleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'fruitables.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'fruitables.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'uz'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ACCOUNT_EMAIL_VERIFICATION = 'none'  # Optional, depends on your needs
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # Optional, can also be 'email' or 'username_email'
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': 'CLIENT_ID',
            'secret': 'SECRET',
            'key': ''
        }
    }
}

