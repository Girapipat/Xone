from flask import Flask, request, jsonify, render_template
from PIL import Image
import numpy as np

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "ไม่มีไฟล์อัปโหลด"}), 400
    
    file = request.files["file"]
    img = Image.open(file.stream).convert("L")  # แปลงเป็น grayscale
    
    # คำนวณค่า intensity เฉลี่ย
    intensity = np.mean(np.array(img))  
    
    # กฎของเบียร์-แลมเบิร์ต (Beer-Lambert Law)
    I0 = 255.0  # ความเข้มแสงเริ่มต้น (สมมติเป็นขาวสว่างสุด)
    I = max(intensity, 1)  # ป้องกันหาร 0
    absorbance = np.log10(I0 / I)
    concentration = absorbance * 10  # factor สมมติ

    return jsonify({
        "intensity": round(float(intensity), 2),
        "absorbance": round(float(absorbance), 4),
        "concentration": round(float(concentration), 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
