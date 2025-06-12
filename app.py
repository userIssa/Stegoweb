from flask import Flask, render_template, request, send_file, redirect
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
EXTRACTED_FOLDER = 'extracted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACTED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/embed', methods=['POST'])
def embed():
    carrier = request.files['carrier']
    secret = request.files['secret']
    password = request.form['password']
    filetype = request.form['filetype']

    carrier_path = os.path.join(UPLOAD_FOLDER, secure_filename(carrier.filename))
    secret_path = os.path.join(UPLOAD_FOLDER, secure_filename(secret.filename))

    carrier.save(carrier_path)
    secret.save(secret_path)

    if filetype == 'audio' and carrier.filename.endswith('.mp3'):
        wav_path = carrier_path.replace('.mp3', '.wav')
        subprocess.run(['ffmpeg', '-y', '-i', carrier_path, wav_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        carrier_path = wav_path

    subprocess.run(['steghide', 'embed', '-cf', carrier_path, '-ef', secret_path, '-p', password, '-sf', carrier_path], input=b'y\n', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return send_file(carrier_path, as_attachment=True)

@app.route('/extract', methods=['POST'])
def extract():
    stegofile = request.files['stegofile']
    password = request.form['password']

    stegopath = os.path.join(UPLOAD_FOLDER, secure_filename(stegofile.filename))
    output_path = os.path.join(EXTRACTED_FOLDER, 'extracted_data')

    stegofile.save(stegopath)

    subprocess.run(['steghide', 'extract', '-sf', stegopath, '-p', password, '-xf', output_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    else:
        return "Extraction failed. Wrong password or file not stego.", 400

if __name__ == '__main__':
    app.run(debug=True)
