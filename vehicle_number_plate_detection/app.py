from flask import Flask, render_template, request
import os
from detector.detect_plate import detect_number_plate

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file uploaded"

    file = request.files['file']
    if file.filename == '':
        return "No file selected"

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    text, output_path = detect_number_plate(file_path)
    return render_template('index.html', result=text, image_path=output_path)

if __name__ == '__main__':
    app.run(debug=True)
