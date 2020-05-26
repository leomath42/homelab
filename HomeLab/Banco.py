#!/usr/bin/python3
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, Session, backref


import sys
import os

engine = create_engine("sqlite:////home/mohelot/projetos/home_lab/bancos/homelab.db", echo=True)
Base = declarative_base()

class UsuarioPermissao(Base):
    __tablename__ = "usuario_permissao"
    idUsuario = Column(Integer, ForeignKey("usuario.id"), primary_key=True)
    idPermissao = Column(Integer, ForeignKey("permissao.id"), primary_key=True)

#     usuario = relationship("Usuario", backref=backref("usuario_permissao"))
#     permissao = relationship("Permissao", backref=backref("usuario_permissao"))

# usuario_permissao = Table('usuario_permissao', Base.metadata,
#     Column('idUsuario', Integer, ForeignKey("usuario.id"), primary_key=True),
#     Column('idPermissao',Integer, ForeignKey("permissao.id"), primary_key=True)
# )
class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    login = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    email = Column(String, nullable=False)
    idAdm = Column(Integer, ForeignKey('usuario.id')) # FOREIGN KEY(idAdm) references usuario(id)
    permissoes = relationship("Permissao", secondary="usuario_permissao", backref=backref("usuarios"),
                              collection_class=set)

    def __init__(self, *args, **kwargs):
        self.__filter__ = kwargs
        # self._update = self.__dict__
        Base.__init__(self, *args, **kwargs)

    # adm = relationship("usuario", back_populates="usuario")

    # static const filter attribute
    def __eq__(self, obj):
        return self.id == obj.id and self.__class__ == obj.__class__

    def __hash__(self):
        return self.id

    def __repr__(self):
        return "<{0}({1})>".format(type(self).__name__, self.id)

    def __columns__(self, columns):
        dic = {}
        for attr, val in self.__dict__.items():
            if attr in columns and val:
                dic[attr] = val
        return dic

    @property
    def _filter(self):
        if not self.__dict__.get('__filter__'):
            # self.__filter__ = {'id': self.id,
            #                    'nome': self.nome,
            #                    'login': self.login,
            #                    'senha': self.senha,
            #                    'email':self.email,
            #                    'idAdm': self.idAdm}
            self.__filter__ = self.__columns__(['id', 'nome', 'login', 'senha', 'email', 'idAdm'])

        return self.__filter__
    
    # dynamic update filter
    @property
    def _update(self):
        # '''
        # retorna os atributos atuais setados no obj.
        # '''
        # __update = self.__dict__.copy()
        # __update.pop('_sa_instance_state')
        # __update.pop('__filter__')
        __update = self.__columns__(['nome', 'login', 'senha', 'email', 'idAdm'])
        return __update

    def serialize(self):
        '''
        serialize serve para serealizar o obj, pode ser usado em sessão,
        diferente do atributo _filter(obs.: não use _filter, pois o mesmo contêm dados
        importantes e não deve estar contido na sessão devido a segurança.
        '''
        return {
            'login': self.login,
            'nome':  self.nome,
            'email': self.email,
            'id':    self.id
        }

    def logar(self, login, password):
        if self.login == login and self.senha == password:
            return True
        else:
            return False

    def cadastrar(self):
        pass

class Arquivo(Base):
    __tablename__ = "arquivo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nomeArquivo = Column(String, nullable=False)
    path = Column(String, nullable=False)
    tipoArquivo = Column(String, nullable=False)
    idPermissao = Column(Integer, ForeignKey("permissao.id"), nullable=False) #FOREIGN KEY(idPermissao) references permissao(id)
    arquivo_tags = relationship("ArquivoTags", back_populates="arquivo")
    permissao = relationship("Permissao", back_populates="arquivos")#, uselist=True, collection_class=set)
    # arquivoTags = None

class ArquivoTags(Base):
    __tablename__ = "arquivo_tags"
    idArquivo = Column(Integer,  ForeignKey("arquivo.id"), primary_key=True, nullable=False)
    idTag = Column(Integer, primary_key=True, nullable=False)
    tag = Column(String, nullable=False) #PRIMARY KEY(idArquivo, idTag)
    arquivo = relationship("Arquivo", back_populates="arquivo_tags")

class Permissao(Base):
    __tablename__ = "permissao"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nivelRestricao = Column(Integer, nullable=False)
    arquivos = relationship("Arquivo", back_populates="permissao")
    # usuarios = relationship("Usuario", secondary=usuario_permissao)

    def __eq__(self, obj):
        return self.id == obj.id and self.__class__ == obj.__class__

    def __hash__(self):
        return self.id

    def __repr__(self):
        return "<{0}({1})>".format(type(self).__name__, self.id)

    # arquivo = relationship("Arquivo", back_populates="permissao")
# Arquivo.arquivoTags = relationship("ArquivoTags", order_by=ArquivoTags.idArquivo, back_populates="arquivo")
# class UsuarioArquivo(Base):
#     idUsuario = Column(Integer, nullable=False)
#     idArquivo = Column(Integer, nullable=False)
#     # PRIMARY KEY(idUsuario, idArquivo),
#     # FOREIGN KEY(idUsuario) references usuario(id),
#     # FOREIGN KEY(idArquivo) references arquivo(id)
#


class Banco(Session):
    '''
    obs.: Talvez seja bom mudar os métodos para staticmethod ou classmethod
    '''
    def __init__(self, bind=None, bind_name=None, echo=True, *args, **kwargs):
        #self.bind = kwargs['engine']
        if bind is None:
            bind = create_engine(bind_name, echo=echo) # return the engine
        elif bind is None and bind_name is None:
            raise AssertionError("bind parameter is None")

        kwargs["bind"] = bind
        super(Banco, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<class '{0}' with id '{1}'>".format(self.__module__ +"."+self.__class__.__name__, id(self))

    def salvarUsuario(self, usuario):
        if isinstance(usuario, Usuario):
            self.add(usuario)
            self.commit()
        else:
            raise TypeError("Objeto passado não é da instância Usuario")

    def consultarUsuario(self, usuario):
        if not isinstance(usuario, Usuario):
            raise TypeError("Objeto passado não é da instância Usuario")
        # recupera entidade usuário
        usuario = self.query(Usuario).filter_by(**usuario._filter).first()
        # init usuario para virar modelo
        # if usuario:
            # usuario = Usuario(id = usuario.id,
            #                   login=usuario.login,
            #                   nome=usuario.nome,
            #                   email=usuario.email,
            #                   senha=usuario.senha,
            #                   idAdm=usuario.idAdm)
            # usuario = Usuario(usuario.__dict__)
        return usuario

    def updateUsuario(self, usuario, **update):
        if not isinstance(usuario, Usuario):
            raise TypeError("Objeto passado não é da instância Usuario")
        print(usuario._update)
        usuario = self.query(Usuario)\
            .filter_by(**usuario._filter)\
            .update(usuario._update, synchronize_session=False)
        self.commit()
        # usuario = Usuario(id=usuario.id,
        #                   login=usuario.login,
        #                   nome=usuario.nome,
        #                   email=usuario.email,
        #                   senha=usuario.senha,
        #                   idAdm=usuario.idAdm)
        # return usuario
if __name__ == "__main__":
    # Session = sessionmaker(bind=engine)
    # Session.configure(bind=engine)
    # session = Session()
    # #Base.metadata.create_all(engine)
    # # usuario = Usuario(id=1, nome="leo", login="leo", senha="123", email="leo@email.com", idAdm=0)
    # # session.add(usuario)
    # arquivo = Arquivo(id=1, nomeArquivo="teste", path="teste", tipoArquivo="teste")
    # # p = Permissao(id=1, nivelRestricao=1)
    # # p.arquivos = [Arquivo(id=1, nomeArquivo="teste", path="teste", tipoArquivo="teste"),
    # #               Arquivo(id=2, nomeArquivo="teste", path="teste", tipoArquivo="teste"),
    # #               Arquivo(id=3, nomeArquivo="teste", path="teste", tipoArquivo="teste")]
    # # arquivo.idPermissao = 2
    # #help(arquivo.permissoes)
    # # arquivo.permissoes = [Permissao(id=1, nivelRestricao=1), Permissao(id=2, nivelRestricao=2)]
    # #arquivo.permissoes = Permissao(id=1, nivelRestricao=1)
    # # arquivo.permissoes.add(Permissao(id=2, nivelRestricao=2))
    # arquivo.permissao = Permissao(id=2, nivelRestricao=2)
    # # arquivo.arquivo_tags
    # # session.add(p)
    # session.add(arquivo)
    # session.commit()
    # session.close()
    from config import config
    banco = Banco(bind_name=config['engine_name'], echo=config['engine_echo'])
    usuario = Usuario(id=2)
    usuario = banco.consultarUsuario(usuario)

    usuario.nome = "nome"
    # usuario.permissoes.add(Permissao(id=4, nivelRestricao=4))
    # usuario.nome = 'testando20'

    '''
        quando troca o id do usuário o ORM substitui o id, mesmo com o filtro de update
    '''
    usuario = Usuario(id=2, nome="")
    # print(usuario.permissoes)
    banco.updateUsuario(usuario)
    # usuario2 = banco.consultarUsuario(usuario)

    # banco.salvarUsuario(usuario2)
    # usuario3 = banco.consultarUsuario(usuario)
    # print(usuario.usuario_permissao)
    # print(usuario.Permissao)
    # b = Banco(engine)
    # print(b.query(Arquivo).all())
    # print(b)
    pass