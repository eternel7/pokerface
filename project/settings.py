"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import json

with open('project/setting.json', 'r') as f:
  config = json.load(f)
  
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['private']['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
  'webpack_loader',
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'oauth2_provider',
  'rest_framework',
  'corsheaders',
  'rest_framework.authtoken',
  'social_django',
  'rest_social_auth',
  'rest_framework_social_oauth2',
  'django_user_agents',
  'accounts',
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'corsheaders.middleware.CorsMiddleware',
  'django.middleware.common.CommonMiddleware',
  'corsheaders.middleware.CorsPostCsrfMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
      os.path.join(BASE_DIR, 'templates'),
    ],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'social_django.context_processors.backends',
        'social_django.context_processors.login_redirect',
      ],
    },
  },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'd2las8b9lr1kdu',
    'USER': 'postgres',
    'PASSWORD': 'grimoire',
    'HOST': 'localhost',
    'PORT': 5432,
  }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
  'DEFAULT_FILTER_BACKENDS': (
    'django_filters.rest_framework.DjangoFilterBackend',
  ),
  'DEFAULT_AUTHENTICATION_CLASSES': (
    'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    'rest_framework_social_oauth2.authentication.SocialAuthentication',
    'rest_framework.authentication.TokenAuthentication',
  ),
}

AUTHENTICATION_BACKENDS = (
  
  # Facebook OAuth2
  'social_core.backends.facebook.FacebookAppOAuth2',
  'social_core.backends.facebook.FacebookOAuth2',
  
  # Google OAuth2
  'social_core.backends.google.GoogleOAuth2',
  
  # Twitter OAuth
  'social_core.backends.twitter.TwitterOAuth',
  
  # django-rest-framework-social-oauth2
  'rest_framework_social_oauth2.backends.DjangoOAuth2',
  
  # Django
  'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_RAISE_EXCEPTIONS = True
SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Facebook configuration
SOCIAL_AUTH_FACEBOOK_KEY = '585737338256884'
SOCIAL_AUTH_FACEBOOK_SECRET = config['private']['SOCIAL_AUTH_FACEBOOK_SECRET']
# Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from facebook.
# Email is not sent by default, to get it, you must request the email permission:
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email'
}

# Google configuration
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '338829541691-14vtulpp1bav75s243cr6cfo0dvojkjl.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config['private']['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']
SOCIAL_AUTH_GOOGLE_OAUTH2_FIELDS = ['email', 'username']
# Twitter configuration
SOCIAL_AUTH_TWITTER_KEY = 'nF5AOvrq4l8FmvjeRgEPpk6ID'
SOCIAL_AUTH_TWITTER_SECRET = 'siZZjbSdoZLI2DnsqOmGcHba92ExtIsI5cJlIsOiNftrzEQz9h'

CSRF_COOKIE_SECURE = True
CORS_ORIGIN_ALLOW_ALL = True

# email configuration
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config['smtp']['server']
EMAIL_PORT = config['smtp']['port']
EMAIL_HOST_USER = config['smtp']['mail']
EMAIL_HOST_PASSWORD = config['smtp']['password']
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'dist'),
  os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'public')
WEBPACK_LOADER = {
  'DEFAULT': {
    'BUNDLE_DIR_NAME': '',
    'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
  }
}
