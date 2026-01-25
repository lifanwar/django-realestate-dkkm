# your_app/widgets.py
from django import forms
from django.utils.safestring import mark_safe

class LeafletCoordinatesWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        # Default Cairo coords
        coords = value or "30.066,31.328"
        lat, lng = coords.split(',') if ',' in coords else ("30.066", "31.328")
        
        return mark_safe(f'''
        <div style="display:flex; gap:10px; align-items:start;">
            <div style="flex:1;">
                <label>Koordinat (Lat, Long):</label><br>
                <input type="text" name="{name}" id="{attrs['id']}" 
                       value="{value or ''}" placeholder="30.077561, 31.336270" 
                       size="50" style="width:100%; padding:5px;" />
            </div>
            <div style="width:450px;">
                <label>Map Preview (klik untuk set):</label><br>
                <div id="mapid_{attrs['id']}" style="width:100%; height:300px; border:1px solid #ddd;"></div>
            </div>
        </div>
        
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
        var map = L.map('mapid_{attrs["id"]}').setView([{lat}, {lng}], 13);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap contributors'
        }}).addTo(map);
        
        var marker = L.marker([{lat}, {lng}]).addTo(map);
        
        // Click map → update input
        map.on('click', function(e) {{
            marker.setLatLng(e.latlng);
            var input = document.getElementById('{attrs["id"]}');
            input.value = e.latlng.lat.toFixed(12) + ', ' + e.latlng.lng.toFixed(12);
        }});
        
        // Edit input → update map
        document.getElementById('{attrs["id"]}').addEventListener('input', function() {{
            var coords = this.value.split(',');
            if (coords.length === 2) {{
                var lat = parseFloat(coords[0].trim());
                var lng = parseFloat(coords[1].trim());
                if (!isNaN(lat) && !isNaN(lng)) {{
                    marker.setLatLng([lat, lng]);
                    map.setView([lat, lng], 15);
                }}
            }}
        }});
        </script>
        ''')
