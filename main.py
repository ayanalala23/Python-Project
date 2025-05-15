from flask import Flask, render_template, request
import cv2
import numpy as np
from PIL import Image
import io

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', result=None)


@app.route('/upload', methods=['POST'])
def upload():
    if 'qrimage' not in request.files:
        return render_template('index.html', result="No file uploaded")

    file = request.files['qrimage']
    if file.filename == '':
        return render_template('index.html', result="No file selected")

    # Read image file as OpenCV format
    in_memory_file = io.BytesIO()
    file.save(in_memory_file)
    data = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)

    # Decode QR
    detector = cv2.QRCodeDetector()
    qr_data, _, _ = detector.detectAndDecode(img)

    if qr_data:
        return render_template('index.html', result=qr_data)
    else:
        return render_template('index.html', result="No QR code detected.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
