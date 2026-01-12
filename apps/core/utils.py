from pathlib import Path
from django.utils.text import slugify


def image_upload_path(instance, filename):
    """
    Generate dynamic upload path menggunakan UUID.
    
    Structure:
    - Gedung: images/gedung_{uuid}/filename.jpg
    - Unit: images/gedung_{gedung_uuid}/unit_{unit_id}/filename.jpg
    """
    # Sanitize filename
    file_path = Path(filename)
    ext = file_path.suffix.lower()
    name = file_path.stem
    safe_name = slugify(name) or 'unnamed'
    safe_filename = f"{safe_name}{ext}"
    
    # Determine path based on content type
    content_type = instance.content_type.model
    
    if content_type == 'gedung':
        from apps.core.models import Gedung
        try:
            gedung = Gedung.objects.get(pk=instance.object_id)
            gedung_uuid = gedung.uuid
            return f'images/gedung_{gedung_uuid}/{safe_filename}'
        except Gedung.DoesNotExist:
            return f'images/temp/{safe_filename}'
        
    elif content_type == 'unit':
        from apps.core.models import Unit
        try:
            unit = Unit.objects.select_related('gedung').get(pk=instance.object_id)
            gedung_uuid = unit.gedung.uuid
            # Slugify unit_number untuk keamanan (contoh: "A-5" jadi "a-5")
            unit_number_slug = slugify(unit.unit_number)
            return f'images/gedung_{gedung_uuid}/{unit_number_slug}/{safe_filename}'
        except Unit.DoesNotExist:
            return f'images/temp/{safe_filename}'
    
    
    return f'images/misc/{safe_filename}'
