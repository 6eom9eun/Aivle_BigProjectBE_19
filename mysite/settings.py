"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
import json
with open(BASE_DIR/'secrets.json') as f:
    secrets = json.loads(f.read())
    
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets['SECRET_KEY']
KAKAO_REST_API_KEY = secrets['KAKAO_REST_API_KEY']
KAKAO_SECRET_KEY = secrets['KAKAO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['aivleteam19literacy.run.goorm.io']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.sites', # registration
    "rest_framework",
    'rest_framework.authtoken',
    'rest_auth',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'rest_framework_simplejwt', # AUTH
    'rest_framework_simplejwt.token_blacklist',
    "allauth",
    "allauth.account",
    'allauth.socialaccount',
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.kakao",
    "allauth.socialaccount.providers.naver",
    'corsheaders',
    'django_filters',
    "accounts",
    "board",
    "rank",
    "study",
]

SITE_ID = 1

# AUTH_USER_MODEL = 'accounts.User'

REST_USE_JWT = True

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username' # username 필드
ACCOUNT_EMAIL_REQUIRED = True            # email 필드 사용 o
ACCOUNT_USERNAME_REQUIRED = False        # username 필드 사용 x
ACCOUNT_AUTHENTICATION_METHOD = 'email'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny', # 누구나 접근
        # 'rest_framework.permissions.IsAuthenticated' # 인증된 사용자만
    ),
}

REST_AUTH = {
    'USE_JWT' : True,
    'JWT_AUTH_COOKIE' : 'access',
    'JWT_AUTH_HTTPONLY': True,
    'JWT_AUTH_REFRESH_COOKIE' : "refresh_token",
    'JWT_AUTH_SAMESITE': 'Lax',
    'JWT_AUTH_COOKIE_USE_CSRF' : False,
    'SESSION_LOGIN' : False
}

SOCIALACCOUNT_PROVIDERS = {
    'kakao': {
        'APP': {
            'client_id': KAKAO_SECRET_KEY,
            'secret': KAKAO_REST_API_KEY,
        }
    },
    'naver': {
        'APP':{
            'clinet_id':secrets['NAVER_CLIENT_ID'],
            'secret': secrets['NAVER_CLIENT_SECRET']
            },
    }
    # 다른 소셜 로그인 제공자 설정도 추가할 수 있음
}

# cookie key 와 refresh cookie key 의 이름을 설정
JWT_AUTH_COOKIE = 'sociallogin-auth'
JWT_AUTH_REFRESH_COOKIE = 'sociallogin-refresh-token'


from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    # 토큰에 들어갈 알고리즘
    'ALGORITHM': 'HS256',
    # 토큰을 만드는데 사용할 secret key
    'SIGNING_KEY': SECRET_KEY,
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [f'{BASE_DIR}/templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application" 


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ko-KR'

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
MEDIA_UTL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"