import socketserver
import datetime
import locale

try:
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'ru_RU')
    except locale.Error:
        print("Warning: Unable to set locale. Using default.")

MOODLE_LOGIN = "1147333"


class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):

        now = datetime.datetime.now()
        formatted_date_time = now.strftime("%d.%m.%Y %H:%M:%S")

        response_text = f"{MOODLE_LOGIN}, {formatted_date_time}\n"

        response = (
                b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: text/plain; charset=utf-8\r\n"
                b"Content-Length: " + str(len(response_text)).encode('utf-8') + b"\r\n"
                                                                                b"\r\n"
                + response_text.encode('utf-8')
        )

        self.request.sendall(response)


HOST, PORT = "127.0.0.1", 8080

with socketserver.TCPServer((HOST, PORT), MyHandler) as server:
    print(f"Server started at http://{HOST}:{PORT}/")
    server.serve_forever()