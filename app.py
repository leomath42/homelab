#!/usr/bin/python3

import json
import os
from flask import Flask, session, render_template, make_response
from flask import request, redirect, url_for, abort
# from sqlalchemy.orm.scoping import scoped_session
from HomeLab.Banco import *
from HomeLab.config import config
from HomeLab.controller import Controller

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

        if Controller.logar(form, session, banco):
            # session["usuario"] = json.dumps(usuario.serialize())
            usuario = Usuario(**session.get('usuario'))
            resp = make_response(redirect(url_for("home", username=usuario.login)))
            resp.set_cookie('usuario', json.dumps(usuario.serialize(), separators=(",", ":")))
            #resp.set_cookie('teste', "{'teste':'teste'}")
            return resp

        else:
            pass
    elif request.method == 'GET' and 'usuario' in session:
        # username = json.loads(session.get('usuario')).get('login')
        usuario = Usuario(**session.get('usuario'))
        return redirect(url_for("home", username=usuario.login))

    return render_template("login.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
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
    if not session.get('usuario') or Usuario(**session.get('usuario')).nome != username:
        abort(404)
    else:
        return render_template("home.html", username=username)

@app.route("/home/commands", methods=['POST'])
def commands():
    form = request.form
    banco = Banco(bind_name=config['engine_name'], echo=config['engine_echo'])

    if not 'usuario' in session:
        abort(404)
    if request.method == 'POST':
        data = form.get("data")
        if data == "sair":
            session.clear() # limpa a sessão atual, obrigando o usuário a logar novamente.
            return "sair"
        elif data == "usuario":
            usuario = Usuario(**session.get('usuario'))
            return render_template('user.html', usuario=usuario)

        elif data == "folder":
            return render_template('folder.html')

        elif data == "update_usuario":
            Controller.updateUser(form, banco)
            return render_template('user.html')

        else:
            return ""
    return render_template('index.html')

@app.route("/home/<username>/sair", methods=['GET','POST'])
def sair(username):
    session.clear()
    return redirect(url_for("login"))

@app.route("/teste")
def teste():
    banco = Banco(bind_name=config['engine_name'], echo=config['engine_echo'])
    usuario = Usuario(id=1)
    usuario = banco.consultarUsuario(usuario)

    return render_template("teste.html", teste=['a', 'b', 'c'])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

# request