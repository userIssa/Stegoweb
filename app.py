from flask import Flask, request, render_template, send_file
import os
from werkzeug.utils import secure_filename
from stegano import lsb
from pydub import AudioSegment
from cryptography.fernet import Fernet
import tempfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Utility: Generate key from password
def generate_key(password):
    return Fernet.generate_key()

# Save typed message as .txt if needed
def save_typed_secret(message):
    fd, path = tempfile.mkstemp(suffix=".txt", dir=app.config['UPLOAD_FOLDER'])
    with os.fdopen(fd, 'w') as tmp:
        tmp.write(message)
    return path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/embed', methods=['POST'])
def embed():
    carrier = request.files['carrier']
    password = request.form['password']
    filetype = request.form['filetype']
    typed_secret = request.form.get('typed_secret', '').strip()
    secret_file = request.files.get('secret')

    carrier_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(carrier.filename))
    carrier.save(carrier_path)

    if secret_file and secret_file.filename:
        secret_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(secret_file.filename))
        secret_file.save(secret_path)
    elif typed_secret:
        secret_path = save_typed_secret(typed_secret)
    else:
        return "Error: Provide either a secret file or typed message.", 400

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'stego_output.png' if filetype == 'image' else 'stego_output.wav')

    # Basic LSB for image (example only)
    if filetype == 'image':
        lsb.hide(carrier_path, message=open(secret_path).read()).save(output_path)
    elif filetype == 'audio':
        # Dummy replacement for actual audio stego
        audio = AudioSegment.from_file(carrier_path)
        audio.export(output_path, format="wav")

    return send_file(output_path, as_attachment=True)

@app.route('/extract', methods=['POST'])
def extract():
    stego = request.files['stegofile']
    password = request.form['password']

    stego_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(stego.filename))
    stego.save(stego_path)

    ext = os.path.splitext(stego.filename)[-1].lower()

    if ext in ['.jpg', '.jpeg', '.png']:
        hidden_msg = lsb.reveal(stego_path)
        if not hidden_msg:
            return "No hidden message found."
        out_path = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_secret.txt')
        with open(out_path, 'w') as f:
            f.write(hidden_msg)
        return send_file(out_path, as_attachment=True)
    elif ext == '.wav':
        return "Audio extraction not implemented in this demo."
    else:
        return "Unsupported file type.", 400

if __name__ == '__main__':
    app.run(debug=True)
