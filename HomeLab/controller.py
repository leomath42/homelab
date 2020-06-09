from HomeLab.model import *
import os
import sys


class Controller:

    @staticmethod
    def logar(form, session, banco):
        login = form.get('login')
        senha = form.get('senha')
        # usuario = banco.consultarUsuario(Usuario(login=login))
        usuario = Usuario(login=login)(banco).find({'login': login})

        if session.get('usuario') or usuario.senha == senha:
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
    def updateUser(form, banco):
        id = form.get('id')
        login = form.get('login')
        nome = form.get('nome')
        email = form.get('email')
        senha = form.get('senha')

        usuario = Usuario(id=id)(banco).find()
        usuario.email = email
        usuario.nome = nome

        if usuario.senha != senha:
            assert Exception("Senha não coincide")
        else:
            usuario(banco).update()

    @staticmethod
    def infoFile(usuario, form, banco):
        id_file = form.get('id')
        arquivo = Arquivo(id=id_file)(banco).find()
        if arquivo in usuario.arquivos:
            return arquivo.serialize()
    @staticmethod
    def upload_file(files, form, session, banco):
        usuario = Usuario(**session.get('usuario'))(banco).find()

        values = files.getlist("fileUpload")
        for file in values:
            # verifica se o usuario esta upando um arquivo já existente no bd.
            if True in [True for arquivo in usuario.arquivos if arquivo.nomeArquivo == file.filename]:
                pass
            else:
                # Salva o Arquivo no /tmp
                file.save('/tmp' + "/" + file.filename)
                if (file.filename.find(".") != -1):
                    tipo = file.filename.split(".")[1]
                else:
                    tipo = ""

                # Cria um Arquivo no banco com as referências do Arquivo salvo em /tmp
                arquivo = Arquivo(nomeArquivo=file.filename, path="/", tipoArquivo=tipo)
                # Adiciona uma permissão default
                arquivo.permissao = Permissao(id=1)(banco).find()  # permissao default
                # Adiciona o arquivo ao usuario corrente(dono do arquivo)
                usuario.arquivos.append(arquivo)
                usuario(banco).update()  # update

    def download_file(self):
        pass