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

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "endpoint_url": f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "endpoint_url": f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        },
    },
}

# #  # # # # # DEVELOPMENT TEST STORAGE # # # # # # #
R2_DEVELOPMENT_URL = os.getenv('R2_DEVELOPMENT_URL')
# Enable Public Bucket for development testing
MEDIA_URL = f"https://pub-{R2_DEVELOPMENT_URL}.r2.dev/"

