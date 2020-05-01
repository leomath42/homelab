#!/usr/bin/python3

import json
import os
from flask import Flask, session, render_template
from flask import request, redirect, url_for, abort
# from sqlalchemy.orm.scoping import scoped_session
from HomeLab.Banco import *
from HomeLab.config import config


app = Flask(__name__)
app.secret_key = os.urandom(16)

# app.config["APPLICATION_ROOT"] = "/home/mohelot/projetos/home_lab/"
# app.config["SESSION_COOKIE_PATH"] = "/home/mohelot/projetos/home_lab/"
# print(app.config)

banco = Banco(bind_name=config['engine_name'], echo=config['engine_echo'])

@app.route("/", methods=['GET', 'POST'])
def login():
    banco = Banco(bind_name=config['engine_name'], echo=config['engine_echo'])
    print(request.form)
    login = password = None

    if request.method == 'POST':

        form = request.form
        login = form['login']
        senha = form['password']

        usuario = Usuario(login=login)
        # print(usuario._filter)
        usuario = banco.consultarUsuario(usuario)

        if usuario is None:
            pass
        elif usuario.logar(form['login'], form['password']):
            session["usuario"] = json.dumps(usuario.serialize())
            return redirect(url_for("home", username=usuario.login))
        else:
            pass
    elif request.method == 'GET' and 'usuario' in session:
        username = json.loads(session.get('usuario')).get('login')
        return redirect(url_for("home", username=username))

    return render_template("login.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    print(session.items())
    # teste
    login = email = password = re_password = None
    if request.method == 'POST':
        form = request.form
        login = form['login']
        email = form['email']
        password = form['password']
        re_password = form['re-password']
        user = Usuario(login=login, nome=login, email=email, senha=password)
        banco.salvarUsuario(user)
    return render_template("signup.html")

@app.route("/home/<username>", methods=['POST', 'GET'])
def home(username):
    if not "usuario" in session:
        abort(404)
    if not username in json.loads(session.get('usuario')).values():
        abort(404)
    if request.method == 'POST':
        print('hello world\n')
    else:
        return render_template("index.html", username=username)

@app.route("/home/commands", methods=['POST'])
def commands():
    if not 'usuario' in session:
        abort(404)
    if request.method == 'POST':
        data = request.form.get("data")
        if data == "sair":
            session.clear() # limpa a sessão atual, obrigando o usuário a logar novamente.
            return "sair"
        elif data == "":
            pass
        else:
            pass
    return render_template('index.html')

@app.route("/home/<username>/sair", methods=['GET','POST'])
def sair(username):
    session.clear()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

# request