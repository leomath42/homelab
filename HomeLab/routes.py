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
    if request.method == 'POST':
        form = request.form

        if Controller.logar(form, session, banco):
            usuario = Usuario(**session.get('usuario'))
            response = make_response(redirect(url_for("home", username=usuario.login)))
            response.set_cookie('usuario', json.dumps(usuario.serialize(), separators=(",", ":")))
            return response
        else:
            template = render_template("login.html", message="senha incorreta ou usuário inexistente.")
            response = make_response(template)
            return response
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
        try:
            banco.salvarUsuario(user)
        except:
            pass
        finally:
            template = render_template("signup.html", form=form,
                                       message="Usuário já existente, por favor, utilize outro login")
            response = make_response(template)
            response.headers['response'] = "error"
            return response

    return render_template("signup.html", form="")


@app.route("/home/<username>", methods=['POST', 'GET'])
def home(username):
    if not session.get('usuario') or Usuario(**session.get('usuario')).login != username:
        abort(404)
    else:
        return render_template("home.html", username=username)


@app.route("/home/commands", methods=['POST'])
def commands():
    form = request.form

    if 'usuario' not in session:
        abort(404)
    if request.method == 'POST':
        data = form.get("data")
        if data == "sair":
            session.clear()  # limpa a sessão atual, obrigando o usuário a logar novamente.
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


@app.route("/home/<username>/sair", methods=['GET', 'POST'])
def sair(username):
    session.clear()
    return redirect(url_for("login"))


@app.route('/home/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # for file in request.files.values():
        #     file.save('/tmp' + "/" + file.filename)
        # return make_response("sucess")            # session["usuario"] = json.dumps(usuario.serialize())
        form = request.form
        files = request.files
        Controller.upload_file(files, form, session, banco)
        return make_response("sucess")


@app.route('/home/download/<path:filename>')
def download_file(filename):
    # send_from_directory é uma função para download de arquivos do Flask
    response = Controller.download_file(filename, send_from_directory, session, banco)
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

# request
