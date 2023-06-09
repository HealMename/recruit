"""
Django settings for dj2 project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import json
import os
from util.configread import config_read

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 读取数据库配置文件
config_file = os.path.join(BASE_DIR, '.env')
with open(config_file) as f:
    config = f.read()
    DATABASES_CONFIG = json.loads(config)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '10086'
SESSION_COOKIE_AGE = 60 * 60 * 24  # token有效期

# 本地
# UPLOAD_URL = "http://127.0.0.1:8087/uploads/"
# web_file_url = "http://127.0.0.1:8087/file/"
# K8S_URL = "http://127.0.0.1:8088/workload/terminal_index/"  # 终端项目
# SMS_API = "http://127.0.0.1:3000/sms/send/"  # 短信接口

# 线上
UPLOAD_URL = "https://www.ittest008.com/uploads/"  # 上传地址
web_file_url = "https://www.ittest008.com/file/"  # 文件域名
K8S_URL = "https://www.ittest008.com/k8workload/terminal_index/"  # 终端项目
SMS_API = "https://www.ittest008.com/sms/send/"  # 短信接口

# 华为云
# UPLOAD_URL = "http://liudeli.top:8087/uploads/"  # 上传地址
# web_file_url = "http://liudeli.top:8087/file/"  # 文件域名
# K8S_URL = "http://liudeli.top:8088/workload/terminal_index/"  # 终端项目
# SMS_API = "http://liudeli.top:3000/sms/send/"  # 短信接口

# REDIS配置
REDIS_HOST = DATABASES_CONFIG['REDIS_HOST']
REDIS_PORT = DATABASES_CONFIG['REDIS_PORT']
REDIS_PASSWORD = DATABASES_CONFIG['REDIS_PASSWORD']
REDIS_DB = DATABASES_CONFIG['REDIS_DB']


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
import logging

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "main",
    "sslserver"
]
MIDDLEWARE = [
    'dj2.mymiddle.CoreMiddle',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',#Forbidden (CSRF cookie not set.)
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'threadlocals.middleware.ThreadLocalMiddleware',
    "xmiddleware.xparam.Xparam",
    "xmiddleware.xauth.Xauth",

]
MEDIA_SITE = os.path.join(BASE_DIR, 'media/')
DB_WAIT_TIMEOUT = 20  # 单个连接最长维持时间
DB_POOL_SIZE = 2  # 连接池最大连接数
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_COOKIE_NAME = "sessionid"
SESSION_COOKIE_PATH = "/"
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = False

ROOT_URLCONF = 'dj2.urls'
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'dj2.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'yclw9@qq.com'
EMAIL_HOST_PASSWORD = 'mhbrkuayvkkgbijd'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
dbName = "django7681v"
DB_ENGINE = 'django.db.backends.mysql'

DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': 'recruit',
        'USER': DATABASES_CONFIG["BASE_USER"],
        'PASSWORD': DATABASES_CONFIG["BASE_PASSWORD"],
        'HOST': DATABASES_CONFIG["BASE_HOST"],
        'PORT': DATABASES_CONFIG["BASE_PORT"],
    },
}
APPEND_SLASH = False
# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/


STATIC_URL = '/assets/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "templates/front/assets"),
]
FILE_URL = "/data/file/"
# media
MEDIA_URL = "/media/"  # 自定义
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 自定义
if os.path.isdir(MEDIA_ROOT) == False:
    os.mkdir(MEDIA_ROOT)

ALIPAY_APP_ID = ''
APP_PRIVATE_KEY_STRING = open('{}/util/alipay_key/app_private_2048.txt'.format(BASE_DIR)).read()
ALIPAY_PUBLIC_KEY_STRING = open('{}/util/alipay_key/alipay_public_2048.txt'.format(BASE_DIR)).read()
ALIPAY_SIGN_TYPE = 'RSA2'


BD_APP_ID = '33687130'
BD_API_KEY = 'HgxU31nWmsqc4eCfg1HAQAe3'
BD_SECRET_KEY = 'jkpL79OWW6UvMhFAwrkh6ptNEzT7HGTz'

