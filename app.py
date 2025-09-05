import os
import numpy as np
from flask import Flask, request, jsonify, render_template
from PIL import Image

app = Flask(__name__)

# ฟังก์ชันคำนวณความเข้มข้น (จำลอง photometer)
def calculate_concentration(image_path):
    img = Image.open(image_path).convert("L")  # แปลงเป็น grayscale
    arr = np.array(img)
    mean_intensity = np.mean(arr)  # ความสว่างเฉลี่ย

    # แปลง intensity (0-255) → mg/L (สมมุติ)
    concentration = (255 - mean_intensity) / 255 * 100  
    return concentration

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected"})

    filepath = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    try:
        concentration = calculate_concentration(filepath)
        return jsonify({"success": True, "concentration": float(concentration)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
