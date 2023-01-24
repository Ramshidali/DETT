from datetime import timedelta
from decouple import config, Csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)
SERVER = config('SERVER', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

INSTALLED_APPS = [
    'registration',
    'mathfilters',
    'el_pagination',
    'rest_framework',
    'versatileimagefield',
    'requests',
    'reportlab',
    'xhtml2pdf',
    'django_inlinecss',

    'dal',
    'dal_select2',
    'mailqueue',

    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',

    'products',
    'general',
    'users',
    'customers',
    'delivery_agents',
    'orders',
    'staffs',
    'promotions',
    'reports',
    'web',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'api.v1.general.exception_handlers.ExceptionMiddleware',
]

ROOT_URLCONF = 'dett.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'general.context_processors.main_context'
            ],
        },
    },
]

WSGI_APPLICATION = 'dett.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    },
}

LOGIN_URL = '/app/accounts/login/'
LOGOUT_URL = '/app/accounts/logout/'
LOGOUT_REDIRECT_URL = ''
LOGIN_REDIRECT_URL = '/app/dashboard/'
LOGIN_ERROR_URL = '/app/accounts/login/'

VERSATILEIMAGEFIELD_SETTINGS = {
    'cache_length': 2592000,
    'cache_name': 'versatileimagefield_cache',
    'jpeg_resize_quality': 70,
    'sized_directory_name': '__sized__',
    'filtered_directory_name': '__filtered__',
    'placeholder_directory_name': '__placeholder__',
    'create_images_on_demand': True,
    'image_key_post_processor': None,
    'progressive_jpeg': False
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=210),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=730),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'EXCEPTION_HANDLER': 'api.v1.general.exception_handlers.handle_exception',
}

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

LANGUAGE_CODE = 'en-us'


TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_ADMIN_MAIL = "muhsinklr55@gmail.com"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = config("EMAIL_USE_TLS")
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = config("EMAIL_PORT")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
DEFAULT_BCC_EMAIL = config("DEFAULT_BCC_EMAIL")
DEFAULT_REPLY_TO_EMAIL = config("DEFAULT_REPLY_TO_EMAIL")
SERVER_EMAIL = config("SERVER_EMAIL")
ADMIN_EMAIL = config("ADMIN_EMAIL")

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = '/static/'
STATIC_FILE_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = (BASE_DIR / 'static',)
STATIC_ROOT = (BASE_DIR / 'static' / 'static_files')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATE_FORMAT = '%d-%m-%y'

PASSWORD_ENCRYPTION_KEY = 'a54MqS4Re_tP6nlVYX6fBBAc025sztJw6URlW35vxCY='
RZP_ID_KEY = 'rzp_test_lXb6SxVILCvIy6'
RZP_SECRET_KEY = 'R4A7PV1MQxgHXKKpeyjGogji'

SITE_URL = ''

