# Menggunakan multi-stage build untuk image yang lebih kecil
FROM python:3.9-slim-buster AS builder

WORKDIR /app

# Install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin kode aplikasi
COPY app .

# Final image
FROM python:3.9-slim-buster

WORKDIR /app

# Salin dependencies dari stage builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app .

EXPOSE 5000

# Perintah untuk menjalankan aplikasi
CMD ["python", "app.py"]