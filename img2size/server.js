const express = require('express');
const multer = require('multer');
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const app = express();
const upload = multer({ dest: 'uploads/' });

// Маршрут для проверки авторства
app.get('/login', (req, res) => {
    res.json({ author: '1147333' });
});

// Маршрут для получения размеров изображения
app.post('/size2json', upload.single('image'), async (req, res) => {
    if (!req.file) {
        return res.status(400).json({ result: 'no file provided' });
    }

    if (!req.file.mimetype.includes('image/png')) {
        return res.status(415).json({ result: 'invalid filetype' });
    }

    try {
        const metadata = await sharp(req.file.path).metadata();
        res.json({ width: metadata.width, height: metadata.height });
    } catch (err) {
        fs.unlinkSync(req.file.path); // Удаляем файл, если произошла ошибка
        return res.status(422).json({ result: 'invalid image' });
    }
});

// Маршрут для отображения HTML-формы
app.use(express.static(path.join(__dirname, 'public')));

app.listen(3000, () => {
    console.log('Server started on http://localhost:3000');
});
