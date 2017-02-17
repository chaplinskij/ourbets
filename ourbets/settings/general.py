"""
Django settings for ourbets project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_3eekp_gau-5au-_)-cst8#(*1ednmbvvcfi_qpl!e$w_ar$qs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'social_django',
    'easy_thumbnails',
    'image_cropping',
    'adminsortable',

    'base',
    'stats',
    'tote',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',
]

from easy_thumbnails.conf import Settings as thumbnail_settings
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

THUMBNAIL_DEBUG = False

ROOT_URLCONF = 'ourbets.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../../base', 'templates')],
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

AUTHENTICATION_BACKENDS = [
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
    # 'social_core.backends.open_id.OpenIdAuth',
    # 'social_core.backends.google.GoogleOpenId',
    # 'social_core.backends.google.GoogleOAuth',
    'django.contrib.auth.backends.ModelBackend',
]

WSGI_APPLICATION = 'ourbets.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../media/')

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'


# Keys and tokens for social API

# GITHUB
SOCIAL_AUTH_GITHUB_KEY = 'Key'
SOCIAL_AUTH_GITHUB_SECRET = 'Secret'

# TWITTER
SOCIAL_AUTH_TWITTER_KEY = 'Key'
SOCIAL_AUTH_TWITTER_SECRET = 'Secret'

# FACEBOOK
SOCIAL_AUTH_FACEBOOK_KEY = 'Key'
SOCIAL_AUTH_FACEBOOK_SECRET = 'Secret'

# VK
SOCIAL_AUTH_VK_OAUTH2_KEY = 'Key'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'Secret'

# GOOGLE
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'Key'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'Secret'

# LINKEDIN
SOCIAL_AUTH_LINKEDIN_KEY = 'Key'
SOCIAL_AUTH_LINKEDIN_SECRET = 'Secret'


#settings for django-social-auth
SOCIAL_AUTH_VK_OAUTH2_EXTRA_DATA = ['screen_name']
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email', 'notify']
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['id', 'email', 'name', 'username']
SOCIAL_AUTH_LOGIN_ERROR_URL = '/settings/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/settings/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False