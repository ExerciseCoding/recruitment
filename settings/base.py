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

import platform
from pathlib import Path

if platform.system() == "Linux" or platform.system() == "Windows":
    # linux or windows
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
elif platform.system() == "Darwin" or platform.system() == "Mac":
    # OS X, 
    # you could not create a folder at /data/logs dure to OS default policy
    LOG_DIR = BASE_DIR
# Application definition

INSTALLED_APPS = [
    # 切换成grappelli主题
    'grappelli',
    'bootstrap4',
    'registration',
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
    'interview',

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
# LDAP_AUTH_URL = "ldap://192.168.1.5:389"
LDAP_AUTH_URL = "ldap://localhost:389"
# LDAP TLS
LDAP_AUTH_USE_TLS = False

LDAP_AUTH_SEARCH_BASE = 'dc=ihopeit, dc=com'

LDAP_AUTH_OBJECT_CLASS = 'inetOrgPerson'

# User model field mapped to the LDAP
# attributes that represent them
LDAP_AUTH_USER_FIELDS = {
    "username": "cn",  # cn: common name
    "first_name": "givenName",
    "last_name": "sn",  # sn: surface name
    "email": "mail",
}

# A tuple of django model fields used to uniquely identify a user
LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",)  # django username作为登录用户

LDAP_AUTH_CLEAN_USER_DATA = "django_python3_ldap.utils.clean_user_data"
LDAP_AUTH_CONNECTION_USERNAME = None
# LDAP_AUTH_CONNECTION_PASSWORD = "JonSn0wbcxnwei3529"
LDAP_AUTH_CONNECTION_PASSWORD = None
# django_python3_ldap.auth.LDAPBackend ldap登录认证的类  django.contrib.auth.backends.ModelBackend: django登录认证
AUTHENTICATION_BACKENDS = {'django_python3_ldap.auth.LDAPBackend', 'django.contrib.auth.backends.ModelBackend'}

# 日志记录

LOGGING = {
    # version: 定义日志记录格式的版本号
    'version': 1,
    # 是否禁用现在已有的其他logger
    'disable_existing_loggers': False,
    # filter过滤器，定义处理链
    # handlers: 处理器日志的处理器，记录到文件还是控制台
    'formatters': {
        'simple': {  # exact format is not important, this is the minimum information
            # asctime: 当前时间 name: 那个类  lineno: 多少行  levelname: 日志级别 message: 消息
            'format': '%(asctime)s %(name)-12s %(lineno)d %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        # 控制台输simple格式
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        # 错误级别的日志发送到邮件
        'mail_admins': {  # Add Handler for mail_admins for `warning` and above
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'file': {
            # 将日志信息记录到文件
            # 'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': os.path.join(LOG_DIR, 'recruitment.admin.log'),
        },

        'performance': {
            # 'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': os.path.join(LOG_DIR, 'recruitment.performance.log'),
        },
    },

    # 系统全级别默认日志记录器
    # 往控制台和文件同时输出
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    # loggers: 日志记录器
    'loggers': {
        "django_python3_ldap": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        },

        "interview.performance": {
            "handlers": ["console", "performance"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# 设为 True，允许用户注册
REGISTRATION_OPEN = True
# 留一周的激活时间；当然，也可以设为其他值
ACCOUNT_ACTIVATION_DAYS = 7
# 设为 True，注册后自动登录
REGISTRATION_AUTO_LOGIN = True
# 登录后呈现给用户的页面
# LOGIN_REDIRECT_URL = '/rango/'
# 未登录以及访问需要验证身份的页面时重定向的页面
LOGIN_URL = '/accounts/login/'
