from django.core.exceptions import ValidationError
from PIL import Image
from pathlib import Path


def validate_image_file(file):
    """Validasi comprehensive untuk image file"""
    # File size
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        raise ValidationError(
            f'Ukuran file terlalu besar. Maksimal {max_size / (1024*1024):.0f}MB'
        )
    
    # Image validation dengan Pillow
    try:
        img = Image.open(file)
        img.verify()
        file.seek(0)
        
        img = Image.open(file)
        width, height = img.size
        
        # Dimensions check
        if width < 100 or height < 100:
            raise ValidationError('Gambar terlalu kecil. Minimal 100x100 pixels')
        
        if width > 5000 or height > 5000:
            raise ValidationError('Gambar terlalu besar. Maksimal 5000x5000 pixels')
        
        # Format check
        allowed_formats = ['JPEG', 'PNG', 'GIF', 'WEBP']
        if img.format not in allowed_formats:
            raise ValidationError(
                f'Format tidak didukung: {img.format}. '
                f'Gunakan: {", ".join(allowed_formats)}'
            )
        
        file.seek(0)
        
    except (IOError, SyntaxError):
        raise ValidationError('File bukan gambar valid atau corrupt')
    
    return file


def validate_filename(filename):
    """Validasi nama file"""
    dangerous_chars = ['..', '/', '\\', '\0', '\n', '\r']
    for char in dangerous_chars:
        if char in filename:
            raise ValidationError('Nama file mengandung karakter berbahaya')
    
    if len(filename) > 255:
        raise ValidationError('Nama file terlalu panjang (max 255 karakter)')
    
    return filename
