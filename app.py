from flask import Flask, request, render_template, jsonify
from PIL import Image
import numpy as np

app = Flask(__name__)

# ค่าการดูดกลืนและความยาวหลอด (ตัวอย่าง)
epsilon = 0.02  # ปรับตามสารจริง
l = 1.0         # cm

def calculate_intensity(img):
    """คืนค่า intensity สูงสุดและค่าเฉลี่ยของภาพ"""
    gray = img.convert('L')
    arr = np.array(gray)
    I0 = arr.max()       # ใช้ค่าพิกเซลสูงสุดแทน reference
    I = arr.mean()       # intensity เฉลี่ย
    return I0, I

def calculate_absorbance(I0, I):
    if I <= 0: I = 0.01  # ป้องกัน log(0)
    return np.log10(I0 / I)

def calculate_concentration(A, epsilon):
    return A / (epsilon * l)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    try:
        file = request.files['file']
        img = Image.open(file)
        I0, I = calculate_intensity(img)
        A = calculate_absorbance(I0, I)
        c = calculate_concentration(A, epsilon)

        return jsonify({
            'intensity_sample': float(I),
            'reference_intensity': float(I0),
            'absorbance': float(A),
            'concentration': float(c)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
