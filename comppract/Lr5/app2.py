import http.server
import socketserver
import datetime
import json
from urllib.parse import urlparse, parse_qs

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("html/form.html", "r", encoding="utf-8") as f:
                self.wfile.write(f.read().encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/":
            content_length = int(self.headers['Content-Length']) # Определяем длину тела запроса
            post_data = self.rfile.read(content_length).decode('utf-8') # Читаем тело запроса
            post_values = parse_qs(post_data) # Разбираем данные из тела запроса

            login = post_values.get("login", [""])[0]  # Получаем значения, default ""
            time = post_values.get("time", [""])[0]

            data = {"login": login, "time": time}

            try:
                with open("data.json", "a", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False)
                    f.write('\n')
            except Exception as e:
                print(f"Ошибка при записи в data.json: {e}")
                self.send_response(500) # Internal Server Error
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
                return

            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8') #Важно, чтобы JS знал
            self.end_headers()
            self.wfile.write("OK".encode('utf-8')) #Простой ответ для JS
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("<html><body><h1>Ошибка 404: Страница не найдена</h1></body></html>".encode('utf-8'))

PORT = 8000
Handler = MyHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server started at port {PORT}")
    try:
         httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped manually.")