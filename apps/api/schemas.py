from ninja import Schema
from typing import Optional, List


class NearbyRequest(Schema):
    """Request schema untuk nearby search"""
    lat: float
    long: float
    radius: int  # dalam meter, 1-1000
    
    class Config:
        json_schema_extra = {
            "example": {
                "lat": 30.054112597729315,
                "long": 31.355256739448002,
                "radius": 500
            }
        }


# Base schema untuk field-field yang sama di Gedung
class GedungBaseSchema(Schema):
    """Base schema untuk gedung (field yang selalu ada)"""
    id: int
    uuid: str
    nama_gedung: Optional[str]
    lat: float
    long: float
    alamat: str
    total_units: int
    primary_image: Optional[str] = None


class GedungSchema(GedungBaseSchema):
    """Schema untuk gedung result dengan distance"""
    distance: float  # jarak dalam meter


class GedungDetailSchema(GedungBaseSchema):
    """Schema untuk gedung detail dengan units (tanpa distance)"""
    units: List['UnitDetailSchema'] = []


class NearbyResponse(Schema):
    """Response schema untuk nearby search"""
    success: bool
    count: int
    radius: int
    center_lat: float
    center_long: float
    results: List[GedungSchema]


class UnitDetailSchema(Schema):
    """Schema untuk unit detail di dalam gedung"""
    id: int
    uuid: str
    lantai: int
    unit_number: str
    deskripsi: str
    alasan_blacklist: Optional[str] = None
    images: List[str] = []


class UnitDetailResponse(Schema):
    """Response schema untuk unit detail lengkap"""
    id: int
    uuid: str
    lantai: int
    unit_number: str
    deskripsi: str
    alasan_blacklist: Optional[str] = None
    gedung_nama: Optional[str]
    listing_type: str
    pemilik: Optional[str] = None
    agen: Optional[str] = None
    images: List[str] = []


class ErrorResponse(Schema):
    """Error response schema"""
    success: bool = False
    error: str


# Rebuild model untuk self-referencing (GedungDetailSchema references UnitDetailSchema)
GedungDetailSchema.model_rebuild()
