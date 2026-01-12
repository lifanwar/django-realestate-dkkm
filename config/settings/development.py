from ..base import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-+1$2))3-1eupo#evj0&b*^doot78v1=6ol^@te6lgp1rk+h(bo')
DEBUG = True
ALLOWED_HOSTS = ['*', '.loca.lt']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
CSRF_TRUSTED_ORIGINS = [
    'https://*.loca.lt',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]