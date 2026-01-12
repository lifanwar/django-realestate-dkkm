from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from pathlib import Path
import shutil
from apps.core.models import Gedung, Unit


@receiver(post_delete, sender=Gedung)
def delete_gedung_folder(sender, instance, **kwargs):
    """
    Hapus folder gedung setelah gedung dihapus
    """
    try:
        gedung_uuid = instance.uuid
        folder_path = Path(settings.MEDIA_ROOT) / 'images' / f'gedung_{gedung_uuid}'
        
        # Hapus folder beserta isinya jika ada
        if folder_path.exists() and folder_path.is_dir():
            shutil.rmtree(folder_path)
            print(f"Folder deleted: {folder_path}")
    except Exception as e:
        print(f"Error deleting folder: {e}")


@receiver(post_delete, sender=Unit)
def delete_unit_folder(sender, instance, **kwargs):
    """
    Hapus folder unit setelah unit dihapus
    """
    try:
        from django.utils.text import slugify
        
        gedung_uuid = instance.gedung.uuid
        unit_number_slug = slugify(instance.unit_number)
        folder_path = Path(settings.MEDIA_ROOT) / 'images' / f'gedung_{gedung_uuid}' / unit_number_slug
        
        # Hapus folder unit jika ada
        if folder_path.exists() and folder_path.is_dir():
            shutil.rmtree(folder_path)
            print(f"Unit folder deleted: {folder_path}")
    except Exception as e:
        print(f"Error deleting unit folder: {e}")
