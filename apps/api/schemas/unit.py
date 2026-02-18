from ninja import Schema
from typing import Optional, List

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