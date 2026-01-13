from math import radians, cos, sin, asin, sqrt
import os
from ninja.security import APIKeyHeader
from ninja.errors import HttpError


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate jarak antara 2 koordinat menggunakan Haversine formula
    Return: jarak dalam meter
    """
    # Convert decimal degrees ke radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius bumi dalam meter
    r = 6371000
    
    return c * r


def get_bounding_box(lat, lon, radius_meters):
    """
    Generate bounding box untuk filter database lebih efisien
    
    Args:
        lat: center latitude
        lon: center longitude
        radius_meters: radius dalam meter
    
    Returns:
        dict: {lat_min, lat_max, lon_min, lon_max}
    """
    # 1 derajat latitude ≈ 111,000 meter
    # 1 derajat longitude ≈ 111,000 * cos(latitude) meter
    
    lat_degree = radius_meters / 111000
    lon_degree = radius_meters / (111000 * cos(radians(lat)))
    
    return {
        'lat_min': lat - lat_degree,
        'lat_max': lat + lat_degree,
        'lon_min': lon - lon_degree,
        'lon_max': lon + lon_degree
    }

# API Keys khusus Imarah Blacklist API (inter-app)
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
