from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# utils
import uuid
from apps.core.utils import image_upload_path
from apps.core.validators import validate_image_file, validate_filename

class BaseModel(models.Model):
    """Abstract base model with timestamp fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Distrik(BaseModel):
    """Model untuk menyimpan data distrik"""
    nama = models.CharField(max_length=100, unique=True, verbose_name='Nama Distrik')
    kode = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name='Kode Distrik (opsional)')
    
    class Meta:
        db_table = 'distrik'
        verbose_name = 'Distrik'
        verbose_name_plural = 'Distrik'
        ordering = ['nama']
    
    def __str__(self):
        return self.nama


class Lokasi(BaseModel):
    """Model untuk menyimpan data lokasi dalam distrik"""
    distrik = models.ForeignKey(Distrik, on_delete=models.CASCADE, related_name='lokasis')
    nama = models.CharField(max_length=200, verbose_name='Nama Lokasi')
    
    class Meta:
        db_table = 'lokasi'
        verbose_name = 'Lokasi'
        verbose_name_plural = 'Lokasi'
        ordering = ['distrik__nama', 'nama']
        unique_together = [['distrik', 'nama']]
    
    def __str__(self):
        return f"{self.nama}, {self.distrik.nama}"


class Gedung(BaseModel):
    """Model untuk menyimpan data gedung"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    lokasi = models.ForeignKey(Lokasi, on_delete=models.CASCADE, related_name='gedungs')
    nama_gedung = models.CharField(max_length=200, blank=True, null=True, help_text='Nama gedung (opsional)')
    lat = models.DecimalField(max_digits=17, decimal_places=15, verbose_name='Latitude', help_text='Contoh: 30.065958719470665')
    long = models.DecimalField(max_digits=18, decimal_places=15, verbose_name='Longitude', help_text='Contoh: 31.327724660547236')
    alamat = models.TextField()
    images = GenericRelation('Image', related_query_name='gedung')
    
    class Meta:
        db_table = 'gedung'
        verbose_name = 'Gedung'
        verbose_name_plural = 'Gedung'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['lat', 'long'])]
    
    def __str__(self):
        return self.nama_gedung or f"Gedung #{self.id}"
    
    @property
    def primary_image(self):
        return self.images.filter(is_primary=True).first()


class Pemilik(BaseModel):
    """Model untuk menyimpan data pemilik"""
    STATUS_CHOICES = [('active', 'Active'), ('blacklist', 'Blacklist')]
    
    nama = models.CharField(max_length=200)
    julukan = models.CharField(max_length=100, blank=True, null=True, verbose_name='Julukan (opsional)', help_text='Nama panggilan atau julukan')
    no_telp = models.CharField(max_length=20, blank=True, null=True, verbose_name='Nomor Telepon (opsional)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='blacklist')
    
    class Meta:
        db_table = 'pemilik'
        verbose_name = 'Pemilik'
        verbose_name_plural = 'Pemilik'
        ordering = ['nama']
    
    def __str__(self):
        return f"{self.nama} ({self.julukan})" if self.julukan else self.nama


class Agen(BaseModel):
    """Model untuk menyimpan data agen"""
    STATUS_CHOICES = [('active', 'Active'), ('blacklist', 'Blacklist')]
    
    nama = models.CharField(max_length=200)
    julukan = models.CharField(max_length=100, blank=True, null=True, verbose_name='Julukan (opsional)', help_text='Nama panggilan atau julukan')
    no_telp = models.CharField(max_length=20, blank=True, null=True, verbose_name='Nomor Telepon (opsional)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='blacklist')
    
    class Meta:
        db_table = 'agen'
        verbose_name = 'Agen'
        verbose_name_plural = 'Agen'
        ordering = ['nama']
    
    def __str__(self):
        return f"{self.nama} ({self.julukan})" if self.julukan else self.nama


class Unit(BaseModel):
    """Model untuk menyimpan data unit properti"""
    LISTING_TYPE_CHOICES = [('available', 'Available'), ('blacklist', 'Blacklist')]
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    gedung = models.ForeignKey(Gedung, on_delete=models.CASCADE, related_name='units')
    pemilik = models.ForeignKey(Pemilik, on_delete=models.SET_NULL, null=True, related_name='units')
    agen = models.ForeignKey(Agen, on_delete=models.SET_NULL, null=True, blank=True, related_name='units')
    deskripsi = models.CharField(max_length=50, verbose_name='Deskripsi', help_text='Contoh: Sebelah kanan, Pintu teralis, di tengah')
    unit_number = models.CharField(max_length=50, verbose_name='Nomor Unit')
    lantai = models.PositiveIntegerField(verbose_name='Lantai', help_text='Lantai unit')
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPE_CHOICES, default='blacklist')
    alasan_blacklist = models.TextField(blank=True, null=True, verbose_name='Alasan Blacklist')
    images = GenericRelation('Image', related_query_name='unit')
    
    class Meta:
        db_table = 'unit'
        verbose_name = 'Unit'
        verbose_name_plural = 'Unit'
        ordering = ['gedung', 'lantai', 'unit_number']
        unique_together = [['gedung', 'unit_number']]
    
    def __str__(self):
        return f"{self.gedung} - Lantai {self.lantai} - Unit {self.unit_number}"
    
    @property
    def primary_image(self):
        return self.images.filter(is_primary=True).first()


class Image(BaseModel):
    """Model polymorphic untuk menyimpan images dari Gedung atau Unit"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': ('gedung', 'unit')})
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to=image_upload_path, help_text='Upload gambar gedung atau unit', validators=[validate_image_file])
    is_primary = models.BooleanField(default=False, verbose_name='Gambar Utama', help_text='Centang jika ini gambar utama')
    
    class Meta:
        db_table = 'image'
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        ordering = ['-is_primary', '-created_at']
        indexes = [models.Index(fields=['content_type', 'object_id'])]
    
    def __str__(self):
        return f"Image for {self.content_object} ({'Primary' if self.is_primary else 'Secondary'})"
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            Image.objects.filter(content_type=self.content_type, object_id=self.object_id, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)
