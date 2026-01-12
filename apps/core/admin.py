from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html
from apps.core.models import Lokasi, Gedung, Pemilik, Agen, Unit, Image, Distrik
from apps.core.forms import GedungAdminForm

# Inline

class ImageInline(GenericTabularInline):
    model = Image
    extra = 1
    fields = ['image', 'is_primary', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.pk and obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Preview'

class LokasiInline(admin.TabularInline):
    model = Lokasi
    extra = 1
    fields = ['nama']

class UnitInline(admin.TabularInline):
    """Inline untuk menampilkan unit di halaman Gedung"""
    model = Unit
    extra = 0
    fields = ['get_detail', 'lantai', 'deskripsi', 'unit_number', 'alasan_blacklist', 'listing_type']
    readonly_fields = ['get_detail', 'lantai', 'unit_number', 'deskripsi', 'alasan_blacklist','listing_type' ]
    max_num = 50
    verbose_name = 'Unit'
    verbose_name_plural = 'Daftar Unit'
    show_change_link = False

    classes = ['collapse'] 

    def get_formset(self, request, obj=None, **kwargs):
        """Override formset untuk hide __str__ link"""
        formset = super().get_formset(request, obj, **kwargs)
        
        # Backup original __str__
        original_str = self.model.__str__
        
        # Override __str__ sementara
        def empty_str(self):
            return ""
        
        # Monkey patch
        self.model.__str__ = empty_str
        
        return formset
    
    def get_detail(self, obj):
        """Link detail ke halaman unit"""
        if obj.pk:
            from django.urls import reverse
            from django.utils.html import format_html
            
            url = reverse('admin:core_unit_change', args=[obj.pk])
            return format_html('<a href="{}">Detail</a>', url)
        return "-"
    
    get_detail.short_description = 'Action'
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Distrik)
class DistrikAdmin(admin.ModelAdmin):
    list_display = ['nama', 'kode', 'created_at']
    search_fields = ['nama', 'kode']
    inlines = [LokasiInline]

@admin.register(Lokasi)
class LokasiAdmin(admin.ModelAdmin):
    list_display = ['nama', 'distrik', 'created_at']
    list_filter = ['distrik']
    search_fields = ['nama', 'distrik__nama']
    autocomplete_fields = ['distrik']



@admin.register(Gedung)
class GedungAdmin(admin.ModelAdmin):
    form = GedungAdminForm
    list_display = ['nama_gedung', 'lokasi', 'alamat', 'lat', 'long', 'created_at']
    list_filter = ['lokasi__distrik', 'created_at']
    search_fields = ['nama_gedung', 'alamat', 'lokasi__lokasi_name']
    autocomplete_fields = ['lokasi']
    list_select_related = ['lokasi']
    inlines = [ImageInline, UnitInline]
    
    fieldsets = (
        ('Informasi Gedung', {
            'fields': ('lokasi', 'nama_gedung', 'alamat')
        }),
        ('Koordinat', {
            'fields': ('coordinates',)
        }),
    )


@admin.register(Pemilik)
class PemilikAdmin(admin.ModelAdmin):
    list_display = ['nama', 'julukan', 'no_telp', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['nama', 'julukan', 'no_telp']


@admin.register(Agen)
class AgenAdmin(admin.ModelAdmin):
    list_display = ['nama', 'julukan', 'no_telp', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['nama', 'julukan', 'no_telp']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['gedung', 'deskripsi', 'unit_number', 'lantai', 'pemilik', 'agen', 'listing_type', 'created_at']
    list_filter = ['listing_type', 'gedung__lokasi__distrik']
    search_fields = ['unit_number', 'gedung__nama_gedung', 'pemilik__nama', 'agen__nama']
    autocomplete_fields = ['gedung', 'pemilik', 'agen']
    list_select_related = ['gedung', 'pemilik', 'agen']
    inlines = [ImageInline]
    
    fieldsets = (
        ('Informasi Unit', {
            'fields': ('gedung', 'deskripsi', 'unit_number', 'lantai', 'pemilik', 'agen')
        }),
        ('Status', {
            'fields': ('listing_type', 'alasan_blacklist')
        }),
    )