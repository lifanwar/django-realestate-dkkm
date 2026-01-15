from ..base import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-+1$2))3-1eupo#evj0&b*^doot78v1=6ol^@te6lgp1rk+h(bo')
DEBUG = True
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('STAGGING_DB_NAME'),
        'USER': os.getenv('STAGGING_DB_USER'),
        'PASSWORD': os.getenv('STAGGING_DB_PASSWORD'),
        'HOST': os.getenv('STAGGING_DB_HOST'),
        'PORT': os.getenv('STAGGING_DB_PORT'),
        'OPTIONS': {
            'sslmode': 'require'
    },
    }
}
CSRF_TRUSTED_ORIGINS = [
    'https://*.loca.lt',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]