from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Gedung


class GedungAdminForm(forms.ModelForm):
    coordinates = forms.CharField(
        label='Koordinat (Lat, Long)',
        help_text='Format: 30.077561674011356, 31.336270654565677',
        required=True,
        widget=forms.TextInput(attrs={
            'size': '50', 
            'placeholder': '30.077561674011356, 31.336270654565677'
        })
    )
    
    class Meta:
        model = Gedung
        fields = '__all__'
        exclude = ['lat', 'long']  # Exclude dari form validation
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial value untuk edit
        if self.instance.pk and self.instance.lat and self.instance.long:
            self.fields['coordinates'].initial = f"{self.instance.lat}, {self.instance.long}"
    
    def clean_coordinates(self):
        """Validasi format koordinat"""
        coords = self.cleaned_data.get('coordinates', '').strip()
        
        if not coords:
            raise ValidationError('Koordinat wajib diisi')
        
        # Validasi format
        pattern = r'^[-+]?[0-9]*\.?[0-9]+\s*,\s*[-+]?[0-9]*\.?[0-9]+$'
        if not re.match(pattern, coords):
            raise ValidationError(
                'Format koordinat salah. Gunakan format: lat, long '
                '(contoh: 30.077561, 31.336270)'
            )
        
        # Validasi nilai
        try:
            lat_str, long_str = coords.split(',')
            lat = float(lat_str.strip())
            long = float(long_str.strip())
            
            if not (-90 <= lat <= 90):
                raise ValidationError('Latitude harus antara -90 dan 90')
            if not (-180 <= long <= 180):
                raise ValidationError('Longitude harus antara -180 dan 180')
            
        except ValueError:
            raise ValidationError('Koordinat harus berupa angka valid')
        
        return coords
    
    def save(self, commit=True):
        """Parse dan assign koordinat ke instance"""
        instance = super().save(commit=False)
        coords = self.cleaned_data.get('coordinates', '').strip()
        
        if coords:
            lat_str, long_str = coords.split(',')
            instance.lat = float(lat_str.strip())
            instance.long = float(long_str.strip())
        
        if commit:
            instance.save()
        
        return instance
