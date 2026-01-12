from ninja import NinjaAPI
from django.db.models import Count, Prefetch
from ninja.errors import HttpError
from .schemas import NearbyRequest, NearbyResponse, UnitDetailResponse, ErrorResponse, GedungDetailSchema
from .utils import haversine_distance, get_bounding_box
from apps.core.models import Gedung, Unit

# utils
import uuid

# Initialize API
api = NinjaAPI(
    title="Imarah Blacklist API",
    version="1.0.0",
    description="API untuk mencari gedung berdasarkan radius lokasi",
    docs_url="/docs"
)


@api.post("/gedung/nearby", response={200: NearbyResponse, 400: ErrorResponse}, tags=["Gedung"])
def search_nearby_gedung(request, payload: NearbyRequest):
    """
    Search gedung dalam radius tertentu dari koordinat.
    
    Algoritma:
    1. Validasi input koordinat dan radius
    2. Hitung bounding box untuk filter database (efisien)
    3. Query gedung yang ada dalam bounding box
    4. Hitung jarak exact menggunakan Haversine
    5. Filter yang benar-benar dalam radius
    6. Sort berdasarkan jarak terdekat
    
    Parameters:
    - lat: Latitude center point (-90 to 90)
    - long: Longitude center point (-180 to 180)
    - radius: Search radius dalam meter (1-1000)
    
    Returns:
    - List gedung dalam radius, sorted by distance
    """
    # 1. Validasi input
    if not (-90 <= payload.lat <= 90):
        raise HttpError(400, "Latitude harus antara -90 dan 90")
    
    if not (-180 <= payload.long <= 180):
        raise HttpError(400, "Longitude harus antara -180 dan 180")
    
    if not (1 <= payload.radius <= 1000):
        raise HttpError(400, "Radius harus antara 1 dan 1000 meter")
    
    # 2. Hitung bounding box untuk filter awal
    bbox = get_bounding_box(payload.lat, payload.long, payload.radius)
    
    # 3. Query gedung dengan bounding box (efisien, tidak get semua gedung)
    gedungs = Gedung.objects.filter(
        lat__gte=bbox['lat_min'],
        lat__lte=bbox['lat_max'],
        long__gte=bbox['lon_min'],
        long__lte=bbox['lon_max']
    ).annotate(
        total_units=Count('units')  # Hitung total unit sekali query
    ).select_related('lokasi').prefetch_related('images')
    
    # 4. Filter exact dengan Haversine dan build response
    results = []
    
    for gedung in gedungs:
        # Hitung jarak exact
        distance = haversine_distance(
            payload.lat, 
            payload.long, 
            float(gedung.lat), 
            float(gedung.long)
        )
        
        # Filter yang benar-benar dalam radius
        if distance <= payload.radius:
            # Get primary image
            primary_img = None
            for img in gedung.images.all():
                if img.is_primary:
                    primary_img = request.build_absolute_uri(img.image.url)
                    break
            
            results.append({
                'id': gedung.id,
                'uuid': str(gedung.uuid),
                'nama_gedung': gedung.nama_gedung,
                'lat': float(gedung.lat),
                'long': float(gedung.long),
                'alamat': gedung.alamat,
                'distance': round(distance, 2),
                'total_units': gedung.total_units,  # Dari annotate
                'primary_image': primary_img
            })
    
    # 5. Sort berdasarkan jarak terdekat
    results.sort(key=lambda x: x['distance'])
    
    # 6. Return response
    return 200, {
        'success': True,
        'count': len(results),
        'radius': payload.radius,
        'center_lat': payload.lat,
        'center_long': payload.long,
        'results': results
    }


@api.get("/gedung/{gedung_uuid}", response={200: GedungDetailSchema, 404: ErrorResponse}, tags=["Gedung"])
def get_gedung_detail(request, gedung_uuid: str):
    """Get detail gedung by UUID with units ordered by lantai"""

    try:
        uuid.UUID(gedung_uuid)
    except ValueError:
        return 404, {"success": False, "error": "not found"}
    
    try:
        gedung = Gedung.objects.annotate(
            total_units=Count('units')
        ).prefetch_related(
            'images',
            Prefetch(
                'units',
                queryset=Unit.objects.prefetch_related('images').order_by('lantai', 'unit_number')
            )
        ).get(uuid=gedung_uuid)
        
        # Get primary image
        primary_img = None
        for img in gedung.images.all():
            if img.is_primary:
                primary_img = request.build_absolute_uri(img.image.url)
                break
        
        # Build units data
        units_data = []
        for unit in gedung.units.all():
            # Get all images for this unit (not just primary)
            unit_images = [
                request.build_absolute_uri(img.image.url) 
                for img in unit.images.all()
            ]
            
            units_data.append({
                'id': unit.id,
                'uuid': str(unit.uuid),
                'lantai': unit.lantai,
                'unit_number': unit.unit_number,
                'deskripsi': unit.deskripsi,
                'alasan_blacklist': unit.alasan_blacklist,
                'images': unit_images
            })
        
        return 200, {
            'id': gedung.id,
            'uuid': str(gedung.uuid),
            'nama_gedung': gedung.nama_gedung,
            'lat': float(gedung.lat),
            'long': float(gedung.long),
            'alamat': gedung.alamat,
            'total_units': gedung.total_units,
            'primary_image': primary_img,
            'units': units_data
        }
    except Gedung.DoesNotExist:
        return 404, {"error": "not found"}

@api.get("/unit/{unit_uuid}", response={200: UnitDetailResponse, 404: ErrorResponse}, tags=["Unit"])
def get_unit_detail(request, unit_uuid: str):
    """Get detail unit by UUID"""
    
    # Validasi UUID
    try:
        uuid.UUID(unit_uuid)
    except ValueError:
        return 404, {"error": "not found"}
    
    try:
        unit = Unit.objects.select_related(
            'gedung', 'pemilik', 'agen'
        ).prefetch_related('images').get(uuid=unit_uuid)
        
        # Get all images
        unit_images = [
            request.build_absolute_uri(img.image.url) 
            for img in unit.images.all()
        ]
        
        # Format pemilik: "Nama (Julukan)"
        pemilik_str = None
        if unit.pemilik:
            if unit.pemilik.julukan:
                pemilik_str = f"{unit.pemilik.nama} ({unit.pemilik.julukan})"
            else:
                pemilik_str = unit.pemilik.nama
        
        # Format agen: "Nama (Julukan)"
        agen_str = None
        if unit.agen:
            if unit.agen.julukan:
                agen_str = f"{unit.agen.nama} ({unit.agen.julukan})"
            else:
                agen_str = unit.agen.nama
        
        return 200, {
            'id': unit.id,
            'uuid': str(unit.uuid),
            'gedung_nama': unit.gedung.nama_gedung,
            'lantai': unit.lantai,
            'unit_number': unit.unit_number,
            'deskripsi': unit.deskripsi,
            'listing_type': unit.listing_type,
            'alasan_blacklist': unit.alasan_blacklist,
            'pemilik': pemilik_str,
            'agen': agen_str,
            'images': unit_images
        }
        
    except Unit.DoesNotExist:
        return 404, {"error": "not found"}

@api.get("/health", tags=["System"])
def health_check(request):
    """Health check endpoint"""
    return {"status": "ok", "message": "API is running"}
