from flask import Flask, render_template, request, jsonify, make_response
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os
import random
import string

app = Flask(__name__)
app.config['MAX_IMAGE_SIZE'] = 5000
app.config['UPLOAD_FOLDER'] = 'static/images'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def generate_filename():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + '.jpg'

def calculate_font_size(width, height):
    return min(int(min(width, height) / 15), 120)

@app.route('/login', methods=['GET'])
def login():
    return jsonify({"author": "1147333"})

@app.route('/')
def home():
    return render_template('makeimage.html')

@app.route('/makeimage', methods=['GET'])
def show_form():
    return render_template('makeimage.html')

@app.route('/makeimage', methods=['POST'])
def generate_image():
    try:
        width = int(request.form.get('width', 0))
        height = int(request.form.get('height', 0))
        text = request.form.get('text', '')[:100].strip()

        if width <= 0 or height <= 0 or width > app.config['MAX_IMAGE_SIZE'] or height > app.config['MAX_IMAGE_SIZE']:
            return render_template('makeimage.html', message="Размеры изображения должны быть от 1 до 5000 пикселей."), 400

        img = Image.new('RGB', (width, height), color=(153, 204, 255))  # Меняем цвет фона на голубой оттенок
        draw = ImageDraw.Draw(img)

        try:
            font_size = calculate_font_size(width, height)
            font = ImageFont.truetype("arial.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()

        # Рассчитываем положение текста с небольшим смещением сверху-вниз
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_x = (width - (text_bbox[2] - text_bbox[0])) // 2
        text_y = (height - (text_bbox[3] - text_bbox[1])) // 2 + font_size // 5
        draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)  # Цвет текста чёрный

        # Сохраняем изображение
        filename = generate_filename()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img.save(filepath, 'JPEG', quality=90)
        image_url = f"/static/images/{filename}"

        return render_template('showimage.html', image_url=image_url)

    except Exception as e:
        return render_template('makeimage.html', message="Что-то пошло не так :(", status_code=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)