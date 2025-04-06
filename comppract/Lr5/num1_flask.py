from flask import Flask
import datetime
import locale

app = Flask(__name__)

MOODLE_LOGIN = "1147333"


try:
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'ru_RU')
    except locale.Error:
        print("Warning: Unable to set locale. Using default.")


@app.route("/")
def hello_world():
    now = datetime.datetime.now()
    formatted_date_time = now.strftime("%d.%m.%y %H:%M:%S")

    return f"{MOODLE_LOGIN}, {formatted_date_time}"


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8000)