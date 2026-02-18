import os
from ninja.security import APIKeyHeader
from ninja.errors import HttpError
        
IMARAH_ALLOWED_API_KEYS = []
api_keys_str = os.getenv('APIKEY_IMARAH_BLACKLIST')
if api_keys_str:
    IMARAH_ALLOWED_API_KEYS = [k.strip() for k in api_keys_str.split(',')]

class ImarahApiKeyAuth(APIKeyHeader):
    param_name = 'X-API-Key'
    
    def authenticate(self, request, key):
        if not IMARAH_ALLOWED_API_KEYS:
            raise HttpError(503, "No API keys configured")
        if key in IMARAH_ALLOWED_API_KEYS:
            return key
        raise HttpError(401, "Invalid")