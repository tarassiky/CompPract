from flask import Flask, jsonify, request, render_template, send_file, redirect, url_for
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from io import BytesIO
import os
import base64  # Import base64
import secrets  # For CSRF token

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # Limit file upload size (2MB)
app.secret_key = secrets.token_hex(16)  # Generate a random secret key for security

# Create a folder for storing the public keys (if needed)
if not os.path.exists('keys'):
    os.makedirs('keys')

# --- Routes ---

@app.route('/')
def index():
    return redirect(url_for('decypher_page'))  # Redirect to the decypher page

@app.route('/decypher')
def decypher_page():
    return render_template('decypher.html')

@app.route('/encrypt')
def encrypt_page():
    return render_template('encrypt.html')

@app.route('/login')
def login():
    return jsonify({"author": "1147333"})

@app.route('/generate_keys', methods=['POST'])
def generate_keys():
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return jsonify({
            "private_key": private_pem.decode('utf-8'),
            "public_key": public_pem.decode('utf-8')
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/encrypt_message', methods=['POST'])
def encrypt_message():
    data = request.get_json()
    public_key_str = data.get('public_key')
    message = data.get('message')

    if not public_key_str or not message:
        return jsonify({"error": "Both public key and message are required"}), 400

    try:
        public_key = serialization.load_pem_public_key(
            public_key_str.encode('utf-8'),
            backend=default_backend()
        )

        encrypted = public_key.encrypt(
            message.encode('utf-8'),
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256(),),
                         algorithm=hashes.SHA256(),
                         label=None)
        )
        return send_file(BytesIO(encrypted), mimetype='application/octet-stream', as_attachment=True, download_name='secret.bin')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/decypher', methods=['POST'])
def decypher():
    if 'key' not in request.files or 'secret' not in request.files:
        return jsonify({"error": "Both key and secret fields are required"}), 400

    key_file = request.files['key']
    secret_file = request.files['secret']

    try:
        private_key_data = key_file.read()
        private_key = serialization.load_pem_private_key(
            private_key_data,
            password=None,
            backend=default_backend()
        )
        encrypted_data = secret_file.read()

        decrypted = private_key.decrypt(
            encrypted_data,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(),
                         label=None)
        )
        return decrypted.decode('utf-8'), 200, {'Content-Type': 'text/plain'}

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) # Listen on all interfaces (for HTTPS) and use port 5000
