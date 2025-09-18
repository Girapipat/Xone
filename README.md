# Photometer Quick Web App

เว็บแอปเลียนแบบ Photometer แบบย่อ: อัปโหลด sample ครั้งเดียว แล้วระบบคำนวณค่า mg/L อัตโนมัติ

## โครงสร้างไฟล์
- app.py : Flask backend
- templates/index.html : UI (TailwindCSS)
- static/js/main.js : ฟังก์ชัน frontend
- calibration.json : ค่า blank และสมการ calibration ตั้งต้น
- requirements.txt : ไลบรารีที่ต้องใช้
- Dockerfile : สำหรับ deploy ด้วย Docker

## วิธีใช้งาน (Local)
```bash
pip install -r requirements.txt
python app.py
```
เปิดเบราว์เซอร์ที่ http://localhost:5000

## วิธีใช้งาน (Docker)
```bash
docker build -t photometer-quick .
docker run -p 5000:5000 photometer-quick
```
"# X" 
"# Zeztz" 
