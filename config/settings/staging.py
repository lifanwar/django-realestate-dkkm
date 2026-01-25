from ..base import *

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
URL = os.getenv('URL_DOMAIN')

DEBUG = False
ALLOWED_HOSTS = [
    f'{URL}',
    ]
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
    f'https://{URL}',
    f'http://{URL}',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Mengaktifkan HSTS dengan waktu tertentu (misalnya 31536000 detik = 1 tahun)
SECURE_HSTS_SECONDS = 31536000  # 1 tahun
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Jika ingin mengaktifkan HSTS untuk subdomain
SECURE_HSTS_PRELOAD = True  # Untuk mendaftarkan domain di preload list HSTS

SESSION_COOKIE_SECURE = False

CSRF_COOKIE_SECURE = False

# cloudflared storage
R2_MEDIA_DOMAIN = os.getenv('R2_MEDIA_DOMAIN')
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')

if not all([R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME]):
    raise ValueError("R2 env vars tidak lengkap!")

# AWS Compatibility settings
AWS_ACCESS_KEY_ID = R2_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = R2_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = R2_BUCKET_NAME
AWS_S3_ENDPOINT_URL = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
AWS_S3_REGION_NAME = "auto"  # ✅ R2 wajib
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False
AWS_S3_CUSTOM_DOMAIN = R2_MEDIA_DOMAIN 

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "endpoint_url": f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = f"https://{R2_MEDIA_DOMAIN}/"