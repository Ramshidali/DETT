### Inside the project named directory (directory that settings.py exists)
### Create a file named settings.ini and paste the following code for first time running.
### Change the database details to your database details.

```

[settings]
; Default details

SECRET_KEY = django-insecure-s0j!w9s4^*3lg1y!d6!!d4@j&z2hew9%%^uu@60i#ixjmdc88y#
DEBUG = True
SERVER = False

ALLOWED_HOSTS= *, .localhost, .127.0.0.1,

; Postgresql details
DB_NAME = dett
DB_USER = postgres
DB_PASSWORD = postgres
DB_HOST = localhost
DB_PORT = 5432


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'developer.talrop@gmail.com'
EMAIL_HOST_PASSWORD = '#helloworld0011'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'Dett <developer.talrop@gmail.com>' 
DEFAULT_BCC_EMAIL = 'developer.talrop@gmail.com'

DEFAULT_REPLY_TO_EMAIL = 'developer.talrop@gmail.com'
SERVER_EMAIL = 'developer.talrop@gmail.com'
ADMIN_EMAIL = 'developer.talrop@gmail.com'


```# DETT
