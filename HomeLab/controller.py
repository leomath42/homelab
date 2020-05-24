from HomeLab.Banco import *

class Controller:

    @staticmethod
    def logar(form, session, banco):
        login = form.get('login')
        senha = form.get('senha')
        usuario = banco.consultarUsuario(Usuario(login=login))

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

        usuario = banco.consultarUsuario(Usuario(id=id))
        usuario.email = email
        usuario.nome = nome

        if usuario.senha != senha:
            assert Exception("Senha não coincide")
        else:
            # usuario_update = Usuario(id=id, login=login, email=email)
            banco.updateUsuario(usuario)