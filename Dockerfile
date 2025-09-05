# ใช้ Python เบาๆ
FROM python:3.10-slim

# ตั้ง working directory
WORKDIR /app

# คัดลอก requirements.txt และติดตั้ง
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมด
COPY . .

# เปิดพอร์ต 5000
EXPOSE 5000

# รัน Flask app
CMD ["python", "app.py"]
