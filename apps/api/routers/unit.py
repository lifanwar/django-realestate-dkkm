import uuid
from ninja import Router

from apps.core.models import Unit
from apps.api.schemas.unit import UnitDetailResponse
from apps.api.schemas.common import ErrorResponse

router = Router()

@router.get("/{unit_uuid}", response={200: UnitDetailResponse, 404: ErrorResponse}, tags=["Unit"])
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