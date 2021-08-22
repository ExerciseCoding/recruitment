"""
Django settings for recruitment project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'blwze5cxv*04oyt(!j%%(xvw%u%i1x%)+gxnq-!*qk_q5fv5vz'

# SECURITY WARNING: don't run with debug turned on in production!
# 可以在控制台看到异常信息
# 生产环境禁用 DEBUG=False
DEBUG = True

# 设置那些IP地址可以访问应用
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Open Ldap
    'django_python3_ldap',
    # 添加新app jobs
    'jobs',
    # interview
    'interview'
]
# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'recruitment.urls'

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

WSGI_APPLICATION = 'recruitment.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'recruitment',
        'USER': 'root',
        'PASSWORD': 'admin',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
           'init_command': 'SET default_storage_engine=INNODB',
           'charset': 'utf8mb4',
        }
    }

}



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# 项目的默认语言 中文:zh-hans 英文:en-us
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# LDAP配置
LDAP_AUTH_URL = "ldap://127.0.0.1:389"
# LDAP TLS
LDAP_AUTH_USE_TLS = False

LDAP_AUTH_SEARCH_BASE = 'dc=ihopeit, dc=com'

LDAP_AUTH_OBJECT_CLASS = 'inetOrgPerson'

# User model field mapped to the LDAP
# attributes that represent them
LDAP_AUTH_USER_FIELDS = {
    "username":"cn",   # cn: common name
    "first_name" : "givenName",
    "last_name": "sn", # sn: surface name
    "email": "mail",
}

# A tuple of django model fields used to uniquely identify a user
LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",)  # django username作为登录用户

LDAP_AUTH_CLEAN_USER_DATA = "django_python3_ldap.utils.clean_user_data"
LDAP_AUTH_CONNECTION_USERNAME = "admin"
LDAP_AUTH_CONNECTION_PASSWORD = "JonSn0wbcxnwei3529"

# django_python3_ldap.auth.LDAPBackend ldap登录认证的类  django.contrib.auth.backends.ModelBackend: django登录认证
AUTHENTICATION_BACKENDS = {'django_python3_ldap.auth.LDAPBackend','django.contrib.auth.backends.ModelBackend'}