from ninja import Router

router = Router()

@router.get("/health", auth=None)
def health_check(request):
    return {"status": "ok", "message": "API is running"}