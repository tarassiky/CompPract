from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
import io
import os

app = Flask(__name__)


# Serve HTML form
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/login')
def login():
    return {"author": "1147333"}


@app.route('/size2json', methods=['GET', 'POST'])
def size2json():
    if 'image' not in request.files:
        return jsonify({"result": "no file provided"}), 400

    file = request.files['image']

    if not file.filename.lower().endswith('.png'):
        return jsonify({"result": "invalid filetype"}), 400

    try:
        img = Image.open(io.BytesIO(file.read()))

        # Проверка, что изображение успешно открыто и имеет размер
        if img.format != 'PNG':
            return jsonify({"result": "invalid filetype"}), 400

        return jsonify({"width": img.width, "height": img.height})
    except Exception as e:
        print(f"Error while processing image: {str(e)}")
        return jsonify({"result": "invalid image"}), 400


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)