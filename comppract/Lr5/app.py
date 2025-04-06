from flask import Flask
from flask import render_template
from flask import request
import datetime
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        login = request.form["login"]
        time = request.form["time"]

        data = {"login": login, "time": time}

        with open("data.json", "a") as f:
            json.dump(data, f)
            f.write('\n')

        message = "Данные успешно сохранены!"
        return render_template("form.html", message=message)

    return render_template("form.html", message=None)

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8000)

