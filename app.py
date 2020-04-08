#!/usr/bin/python3

from flask import Flask, render_template
from flask import request


app = Flask(__name__)
app.config["APPLICATION_ROOT"] = "/home/mohelot/projetos/home_lab/"


@app.route("/", methods=['GET', 'POST'])
def home():
    print(request.form)
    return render_template("home.html")


@app.route("/index")
def index():
    # teste
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
