# Gunakan image Python
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Salin requirements.txt dan instal dependensi
COPY requirements.txt .
RUN pip install -r requirements.txt

# Salin seluruh aplikasi ke dalam kontainer
COPY . .

# Set environment variable untuk Django settings
ENV DJANGO_SETTINGS_MODULE=config.settings.staging

# Expose port untuk Django
EXPOSE 8000

# Jalankan aplikasi menggunakan Gunicorn
CMD ["gunicorn", "--workers=3", "config.wsgi:application", "--bind", "0.0.0.0:8000"]