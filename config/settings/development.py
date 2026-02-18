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

# cloudflared storage
R2_MEDIA_DOMAIN = os.getenv('R2_MEDIA_DOMAIN')
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')

if not all([R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME]):
    raise ValueError("R2 env vars tidak lengkap!")

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "endpoint_url": f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
            "access_key": R2_ACCESS_KEY_ID,  # Opsional, baca dari env
            "secret_key": R2_SECRET_ACCESS_KEY,
            "bucket_name": R2_BUCKET_NAME,
            "region_name": "auto",
            "default_acl": None,  # Ganti dari AWS_DEFAULT_ACL
            "file_overwrite": False,  # Ganti dari AWS_S3_FILE_OVERWRITE
            "custom_domain": R2_MEDIA_DOMAIN,
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = f"https://{R2_MEDIA_DOMAIN}/"