from ninja import Schema

class ErrorResponse(Schema):
    """Error response schema"""
    success: bool = False
    error: str