#!/usr/bin/python3
import json
from flask import session, render_template, make_response
from flask import request, redirect, url_for, abort, send_from_directory
from HomeLab.model import *
from HomeLab.controller import Controller
from HomeLab import database as db

from HomeLab import app

banco = db

# app.config["APPLICATION_ROOT"] = "/home/mohelot/projetos/home_lab/"
# app.config["SESSION_COOKIE_PATH"] = "/home/mohelot/projetos/home_lab/"
# app.config['SQLALCHEMY_DATABASE_URI'] = bind_name=config['engine_name']

# banco = db
@app.route("/", methods=['GET', 'POST'])
def login():
    # banco = Banco(bind_name=config['engine_name'], echo=config['engine_echo'])
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
    if not session.get('usuario') or Usuario(**session.get('usuario')).login != username:
        abort(404)
    else:
        return render_template("home.html", username=username)

@app.route("/home/commands", methods=['POST'])
def commands():
    form = request.form
    # banco = Banco(bind_name=config['engine_name'], echo=config['engine_echo'])

    if not 'usuario' in session:
        abort(404)
    if request.method == 'POST':
        data = form.get("data")
        if data == "sair":
            session.clear() # limpa a sessão atual, obrigando o usuário a logar novamente.
            return "sair"
        elif data == "usuario":
            usuario = Usuario(**session.get('usuario'))(banco).find()
            return render_template('user.html', usuario=usuario)

        elif data == "folder":
            usuario = Usuario(**session.get('usuario'))(banco).find()
            return render_template('folder.html', arquivos=usuario.arquivos)

        elif data == "update_usuario":
            Controller.updateUser(form, banco)
            return render_template('user.html')
        elif data == "info_file":
            usuario = Usuario(**session.get('usuario'))(banco).find()
            return Controller.infoFile(usuario, form, banco)
        else:
            return ""
    return render_template('index.html')

@app.route("/home/<username>/sair", methods=['GET','POST'])
def sair(username):
    session.clear()
    return redirect(url_for("login"))

@app.route("/teste", methods=['GET', 'POST'])
def teste():
    # banco = Banco(bind_name=config['engine_name'], echo=config['engine_echo'])
    usuario = Usuario(id=1)
    usuario = banco.consultarUsuario(usuario)
    if request.method == 'POST':
        if request.form.get('teste') == 'teste':
            file = request.files['file']
            file.save('/tmp/upload_file.txt')
        elif request.form.get('download') == 'download':
            return redirect('/download/upload_file.png')
    return render_template("teste.html", teste=['a', 'b', 'c'])

@app.route('/home/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        # for file in request.files.values():
        #     file.save('/tmp' + "/" + file.filename)
        # return make_response("sucess")
        # banco = Banco(bind_name=config['engine_name'], echo=config['engine_echo'])
        form = request.form
        files = request.files
        Controller.upload_file(files, form, session, banco)
        return make_response("sucess")

@app.route('/home/download/<path:filename>')
def download_file(filename):
    return send_from_directory('/tmp', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

# request