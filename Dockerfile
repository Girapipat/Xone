# ใช้ image เบาๆ ของ Python
FROM python:3.10-slim

# ติดตั้ง dependencies ระดับระบบที่ Pillow อาจต้องใช้
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# คัดลอก requirements แล้วติดตั้ง
COPY requirements.txt .

# ติดตั้ง Python packages (รวม gunicorn สำหรับ production)
RUN pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir gunicorn

# คัดลอกโค้ดแอปทั้งหมด
COPY . .

# สร้างโฟลเดอร์เก็บภาพที่อัปโหลด
RUN mkdir -p /app/uploads

# สร้าง user ไม่รันเป็น root
RUN addgroup --system appgroup \
 && adduser --system --ingroup appgroup appuser \
 && chown -R appuser:appgroup /app

# พอร์ต default (สามารถ override ด้วย env var เวลารัน)
ENV PORT=5000
EXPOSE 5000

# Healthcheck (ติดตั้ง curl ด้านบน)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s CMD curl -f http://localhost:${PORT}/ || exit 1

# รันด้วย non-root user
USER appuser

# คำสั่งเริ่มต้น ใช้ gunicorn เพื่อรัน WSGI app (app.py ต้องมีตัวแปร `app`)
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT} --workers 2 --threads 2 --timeout 30"]
