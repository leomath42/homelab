#!/usr/bin/python3
import json
import os

from flask import session, render_template, make_response
from flask import request, redirect, url_for, abort, send_from_directory
from HomeLab.model import *
from HomeLab.controller import Controller
from HomeLab.controller import Device as controller_Device
from HomeLab.controller import devices as controller_devices
from HomeLab import util
from HomeLab import database as db
from HomeLab.config import config

from HomeLab import app

banco = db

# load json config device file as dict and add to session
# for no render every request.
# with open(os.path.join(config['homelab_path'], 'config', 'device.json'), "r") as file:
#     session['device_config'] = json.load(file)

# load template to session for no render every request.
    ##################################################

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
        confirm = form['re-password']
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


@app.route("/home/<username>/folder", methods=['GET', 'POST'])
def folder(username):
    form = request.form
    usuario = Usuario(**session.get('usuario'))(banco).find()
    for arquivo in usuario.arquivos:
        util.format_file(arquivo)
    return render_template('folder.html', username=username, arquivos=usuario.arquivos)


@app.route("/home/<username>/user", methods=['GET', 'POST'])
def user(username):
    form = request.form
    usuario = None
    if request.method == 'GET':
        usuario = Usuario(**session.get('usuario'))(banco).find()

    elif request.method == 'POST':
        usuario = Controller.updateUser(form, session, banco)

    return render_template('user.html', username=username, usuario=usuario)

@app.route("/home/commands", methods=['POST'])
def commands():
    form = request.form
    usuario = Usuario(**session.get('usuario'))(banco).find()

    if 'usuario' not in session:
        abort(404)
    if request.method == 'POST':
        data = form.get("data")

        if data == "update_usuario":
            Controller.updateUser(form, banco)
            return render_template('user.html')

        elif data == "info_file":
            info = Controller.infoFile(usuario, form, banco)
            # adiciona a data formatada e remove a data não formatada
            info['date'] = util.format_time(info['time'])
            info.pop('time')
            return info

        elif data == "print":
            return render_template('print.html', printers=[])

        elif data == "devices":
            templates_devices = None
            return render_template('devices.html', devices=templates_devices)

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


@app.route('/home/delete/<int:idFile>', methods=['GET', 'POST', 'DELETE'])
def delete_file(idFile):
    response = make_response('sucesso.')
    if not Controller.delete_file(idFile, session, banco):
        response = make_response('erro, arquivo não existe.')
    return response


@app.route("/home/print/<int:idFile>", methods=['POST'])
def print_file(idFile):
    '''
        depois essa gambiarra irá ser mudado por uma configuração via xml kkkk xD
    '''
    arquivo = Arquivo(id=idFile)(db).find()
    remote_host = "192.168.0.24"
    remote_printer = "Photosmart_C4700_series"
    command = "lp -h {0} -d{1} {2}"

    local_file = os.path.join(config['data_path'], arquivo.nomeArquivo)

    command = command.format(remote_host, remote_printer, local_file)
    output = os.popen(command, 'r')._stream.readlines()[0]
    response = make_response(output)
    return response

# @app.route("/home/folder", methods=['GET', 'POST'])
# def folder():
#     return render_template('teste.xml')

@app.route('/home/<username>/devices', methods=['GET', 'POST', 'PUT', 'DELETE'])
def devices(username):
    form = request.form
    if request.method == "POST":
        device_type = form['device_type']
        device_template = form['device_button_type']

        device = Dispositivo()
        device.template = device_template
        device.funcao = "device"
        permission = Permissao(id=4)(db).find()
        device.idPermissao = permission.id
        device(db).save()

        with open(os.path.join(config['homelab_path'], 'config', 'device.json'), "r+") as file:
            _device_dict = {'descriptor': form['descriptor'], 'connect_type': form['connect_type'],
                     'address': form['address'], 'port': form['port'], 'serial': form['serial']}
            _json_dict = json.load(file)
            _json_dict[device.id] = _device_dict
            file.seek(0)
            # session['device_config']
            json.dump(_json_dict, file)

    # atualiza as informações de um dispositivo em específico.
    if request.method == 'PUT':
        _id = form['id']


    # elif request.method == "GET":
    #     # device = Dispositivo(id=1)(db).find()
    #     # device2 = Dispositivo(id=2)(db).find()
    #     # device_template = util.generate_device_template_from_xml('config.xml', device.id)
    #     # device_template = util.Template(device)
    #     # device.template = device_template
    #     # template = Template('button-1', 'button-1', 'button')
    #     # device = render_template('device_template.html', device=template)
    #     # return render_template('devices.html', username=username, device=device)
    devices = db.query(Dispositivo).all()

    return render_template('devices.html', username=username, devices=devices)

# @app.errorhandler(werkzeug.exceptions.BadRequest)
@app.route("/device/<int:id_device>", methods=['POST', 'GET', 'PUT', 'DELETE'])
def device(id_device):

    if request.method == 'GET':
        device = Dispositivo(id=id_device)(db).find()
        with open(os.path.join(config['homelab_path'], 'config', 'device.json'), "r") as file:
            dic = json.load(file)
            device_config = dic.get(str(device.id))

        device_json = device.serialize()
        # device_json['config'] = device_config
        device_json.update(device_config)

        return device_json

    elif request.method == 'POST':
        pass

    elif request.method == 'PUT':
        # busca device
        device = Dispositivo(id=id_device)(db).find()

        _json = request.json
        device.idPermissao = _json["idPermissao"]
        device.funcao = _json["funcao"]
        device.template = _json["template"]

        # muda as configurações que estão em device.json.
        with open(os.path.join(config['homelab_path'], 'config', 'device.json'), 'r+') as file:
            file_as_json = json.load(file)
            file_as_json[str(device.id)] = {
                _json["descriptor"],
                _json["connect_type"],
                _json["address"],
                _json["port"],
                _json["serial"]
            }
            file.seek(0)
            json.dump(file_as_json, file)

        device(db).save()

    elif request.method == 'DELETE':
        device = Dispositivo(id=id_device)(db).find()

        # remove a configuração que está em device.json associada ao id do device
        with open(os.path.join(config['homelab_path'], 'config', 'device.json'), 'r+') as file:
            file_as_json = json.load(file)
            file_as_json.pop(str(device.id))
            file.seek(0)
            json.dump(file_as_json, file)

        device.remove()

# return {'teste':'teste'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

# request
