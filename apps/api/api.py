from ninja import NinjaAPI

from apps.api.auth import ImarahApiKeyAuth
from apps.api.routers.gedung import router as gedung_router
from apps.api.routers.unit import router as unit_router
from apps.api.routers.system import router as system_router

api = NinjaAPI(
    title="Imarah Blacklist API",
    version="1.0.1",
    description="API untuk mencari gedung berdasarkan radius lokasi",
    docs_url="/docs",
    auth=ImarahApiKeyAuth(),
)

api.add_router("/gedung", gedung_router, tags=["Gedung"])
api.add_router("/unit", unit_router, tags=["Unit"])
api.add_router("", system_router, tags=["System"])