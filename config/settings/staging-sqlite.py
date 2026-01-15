from ..base import *

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = False
ALLOWED_HOSTS = ['dkkm.jastipin.id']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
CSRF_TRUSTED_ORIGINS = [
    'https://dkkm.jastipin.id',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Mengaktifkan HSTS dengan waktu tertentu (misalnya 31536000 detik = 1 tahun)
SECURE_HSTS_SECONDS = 31536000  # 1 tahun
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Jika ingin mengaktifkan HSTS untuk subdomain
SECURE_HSTS_PRELOAD = True  # Untuk mendaftarkan domain di preload list HSTS

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True