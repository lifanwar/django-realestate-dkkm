from pathlib import Path
from django.utils.text import slugify
from django.utils.html import strip_tags


def image_upload_path(instance, filename):
    """
    Generate dynamic upload path menggunakan nama_gedung (slug).
    
    Structure:
    - Gedung: images/gedung_[nama-slug]_[date]/filename.jpg
    - Unit: images/gedung_[nama-slug]_[date]/unit_[unit_id]/filename.jpg
    """
    # Sanitize filename
    file_path = Path(filename)
    ext = file_path.suffix.lower()
    name = file_path.stem
    safe_name = slugify(name)[:50] or 'unnamed'  # Max 50 chars
    safe_filename = f"{safe_name}{ext}"
    
    # Date folder (optional, anti collision)
    from datetime import datetime
    date_folder = datetime.now().strftime('%Y/%m')
    
    # Determine path based on content type
    content_type = instance.content_type.model
    
    if content_type == 'gedung':
        from apps.core.models import Gedung
        try:
            gedung = Gedung.objects.get(pk=instance.object_id)
            
            # Slug dari nama_gedung (max 30 chars, aman untuk URL)
            gedung_slug = slugify(strip_tags(gedung.nama_gedung or f'gedung-{gedung.id}'))[:30]
            if not gedung_slug:
                gedung_slug = f'gedung-{gedung.id}'
                
            return f'images/gedung_{gedung_slug}/{date_folder}/{safe_filename}'
            
        except Gedung.DoesNotExist:
            return f'images/temp/{date_folder}/{safe_filename}'
        
    elif content_type == 'unit':
        from apps.core.models import Unit
        try:
            unit = Unit.objects.select_related('gedung').get(pk=instance.object_id)
            
            # Gedung slug
            gedung_slug = slugify(strip_tags(unit.gedung.nama_gedung or f'gedung-{unit.gedung.id}'))[:30]
            if not gedung_slug:
                gedung_slug = f'gedung-{unit.gedung.id}'
            
            # Unit slug
            unit_slug = slugify(unit.unit_number or f'unit-{unit.id}')[:20]
            
            return f'images/gedung_{gedung_slug}/{date_folder}/{unit_slug}/{safe_filename}'
            
        except Unit.DoesNotExist:
            return f'images/temp/{date_folder}/{safe_filename}'
    
    return f'images/misc/{date_folder}/{safe_filename}'
