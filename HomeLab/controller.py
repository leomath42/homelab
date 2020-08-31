import os
import socket
import time

import serial

from HomeLab import database as db
from HomeLab import util
from HomeLab.config import config
from HomeLab.model import *

import traceback


class Controller:

    @staticmethod
    def logar(form, session, banco):
        login = form.get('login')
        senha = form.get('password')
        # usuario = banco.consultarUsuario(Usuario(login=login))
        usuario = Usuario(login=login)(banco).find({'login': login})

        if not usuario:
            return False

        elif session.get('usuario') or usuario.senha == senha:
            session['usuario'] = usuario.serialize()
            return True
        # elif not usuario:
        #     return False
        else:
            return False

    @staticmethod
    def cadastrar():
        pass

    @staticmethod
    def updateUser(form, session, banco):
        _id = session.get('usuario').get('id')
        login = form.get('login')
        nome = form.get('nome')
        email = form.get('email')
        senha = form.get('senha')

        usuario = Usuario(id=_id)(banco).find()
        usuario.email = email
        usuario.nome = nome

        if usuario.senha != senha:
            assert Exception("Senha não coincide")

        return usuario(banco).update()

    @staticmethod
    def infoFile(usuario, form, banco):
        id_file = form.get('id')
        arquivo = Arquivo(id=id_file)(banco).find()
        if arquivo in usuario.arquivos:
            return arquivo.serialize()

    @staticmethod
    def upload_file(files, form, session, banco):
        usuario = Usuario(**session.get('usuario'))(banco).find()

        def fileSize(file):
            # 'seek' pula pro primeiro byte do final do arquivo
            file.seek(0, 2)
            # recupera o tamanho do arquivo
            size = file.tell()
            # volta ao inicio do arquivo para poder salvar
            file.stream.seek(0, 0)
            K = 10 ** 3
            M = 10 ** 6
            G = 10 ** 9
            formated_size = ""
            if K < size < M:
                formated_size = "%.2f" % (size / K) + "KB"
            elif M < size < G:
                formated_size = "%.2f" % (size / M) + "MB"
            elif size > G:
                formated_size = "%.2f" % (size / G) + "GB"
            else:
                formated_size = size + " B"

            return formated_size

        values = files.getlist("fileUpload")
        for file in values:
            # verifica se o usuario esta upando um arquivo já existente no bd.
            if True in [True for arquivo in usuario.arquivos if arquivo.nomeArquivo == file.filename]:
                pass
            else:
                size = fileSize(file)
                # Salva o Arquivo no /tmp
                file.save(os.path.join(config['data_path'], file.filename))

                if file.filename.find(".") != -1:
                    tipo = file.filename.split(".")[1]
                else:
                    tipo = ""

                # Cria um Arquivo no banco com as referências do Arquivo salvo em /tmp
                arquivo = Arquivo(nomeArquivo=file.filename, path="/", tipoArquivo=tipo, size=size, time=time.time())
                # Adiciona uma permissão default
                arquivo.permissao = Permissao(id=1)(banco).find()  # permissao default
                # Adiciona o arquivo ao usuario corrente(dono do arquivo)
                usuario.arquivos.append(arquivo)
                usuario(banco).update()  # update

    @staticmethod
    def download_file(filename, downloadFunction, session, banco):
        #   verificar se o usuário possui permissão para fazer download
        #   e se possui permissão para fazer download do arquivo passado.
        #
        file = downloadFunction(config['data_path'], filename, as_attachment=True)
        return file

    @staticmethod
    def delete_file(idFile, session, banco):
        try:
            arquivo = Arquivo(id=idFile)(banco).find()
            assert arquivo is not None

            filename = os.path.join(config['data_path'], arquivo.nomeArquivo)
            # os.path.exists(filename):
            os.remove(filename)
            arquivo(banco).remove()
        except(AssertionError, FileNotFoundError):
            import traceback.print_exec as traceback
            traceback()
            return False
        finally:
            return True


class Device(object):
    """
        Documentação:
        Device
    """

    def __init__(self, id, descriptor, connect_type, model_class=None, address=None, port=None, serial_port=None,
                 **kwargs):
        """

        @type id: object
        """
        self.id = int(id) # converte de str|int para int
        self.descriptor = descriptor
        self._connect_type = connect_type
        self.address = address
        self.port = int(port) if port else None
        self.serial_port = serial_port
        self._model_class = model_class
        # assert isinstance(model_class, HomeLab.model.Model)

        # adiciona outras variáveis ex.: baudrate

        # self.__dict__.update(kwargs)
        self._serial = None
        self._inet = None
        self._connect = None
        self.connected = False

        self.max_block_message = int(kwargs.get('max_block_message')) if kwargs.get('max_block_message') else 8
        # init _connect
        self.connect_type = self._connect_type

    @property
    def connect_type(self):
        return self._connect_type

    @connect_type.setter
    def connect_type(self, connect_type):
        self._connect_type = connect_type

        # talvez seja interessante tornar serial_port, port, address e outros atributos como property
        # para funcionar da mesma forma que connect_type, assim sempre que atualizar algum atributo o _connect
        # ira atualizar também e o método connect irá funcionar da mesma forma.

        __connect = None
        if connect_type == 'serial':
            def _connect():
                self._serial = serial.Serial(port=self.serial_port)

            __connect = _connect

        elif connect_type == 'inet':
            def _connect():
                self._inet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._inet.connect((self.address, self.port))

            __connect = _connect

        self._connect = __connect

    @property
    def model_class(self):
        return self._model_class

    @model_class.setter
    def model_class(self, model_class):
        assert isinstance(model_class, Model)
        self._model_class = model_class

    def __getattribute__(self, item):
        __dict__ = object.__getattribute__(self, '__dict__')
        model_class = __dict__.get('model_class')
        if __dict__.get(item):
            value = __dict__.get(item)
        elif model_class and model_class.__dict__.get(item):
            value = model_class.__dict__.get(item)
        else:
            value = object.__getattribute__(self, item)

        return value

    def connect(self):
        # if self.connect_type == 'serial':
        #     self.serial = serial.Serial(port=self.serial_port)
        #
        # elif self.connect_type == 'inet':
        #     self.inet = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #     self.inet.connect((self.address, self.port))
        try:
            self._connect()
            self.connected = not self.connected
        except:
            # tentativa de tratamento de erro aqui.
            traceback.print_exc()

        return self.connected

    def send(self, message):
        block_message = str('send' + self.descriptor + message).encode()

        # evita enviar uma carga de payload muito grande ao microcontrolador, etc.
        assert not len(block_message) > self.max_block_message

        if self.connect_type == 'serial':
            self._serial.write(block_message)

        elif self.connect_type == 'inet':
            with self._inet as inet:
                inet.send(block_message)
                self.connected = not self.connected

    def receive(self):
        pass


class Printer(Device):

    def __init__(self, *args, **kwargs):
        def __getargs(name, index, *args, **kwargs):
            return kwargs.get(name) if kwargs.get(name) else args[index] if len(args) > index else None

        self.id = __getargs('id', 0, *args, **kwargs)
        self.host = __getargs('host', 1, *args, **kwargs)
        self.printerName = __getargs('printerName', 2, *args, **kwargs)
        self.commandFormat = __getargs('commandFormat', 3, *args, **kwargs)
        self.message = __getargs('message', 4, *args, **kwargs)

    def do_print(self, file_name, **kwargs):
        command = self.commandFormat.format(self.host, self.printerName, file_name)
        print(command)
        os.popen(command)

    def cancel_print(self):
        pass

    def format_print(self, *args, **kwargs):
        pass


def _func_device(obj):
    d = Dispositivo(id=obj.id)(db).find()
    obj.model_class = d
    obj.connect()


def _func_printer(obj):
    p = Printer(id=obj.id)(db).find()
    obj.model_class = p
    obj.connect()


devices = util.parse_xml_to_object_list('config.xml', Device, None)
printers = util.parse_xml_to_object_list('config.xml', Device, None)

__all__ = ['Printer', 'Device', 'Controller']
