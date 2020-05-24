from HomeLab.Banco import *

class Controller:

    @staticmethod
    def logar():
        pass

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

        usuario = banco.consultarUsuario(Usuario(id=id))
        usuario.email = email
        usuario.nome = nome

        if usuario.senha != senha:
            assert Exception("Senha não coincide")
        else:
            # usuario_update = Usuario(id=id, login=login, email=email)
            banco.updateUsuario(usuario)