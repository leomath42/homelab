#!/usr/bin/python3
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, update
from sqlalchemy.orm import relationship, backref
from abc import ABC, abstractmethod
import sys, os, traceback
from sqlalchemy.orm import scoped_session

Base = declarative_base()


class Handler(object):
    def __init__(self, entity, session_object):
        self.session = session_object
        self.entity = entity

    def __repr__(self):
        return "<Handler-({0}-{1})>".format(self.entity, self.session)

    def find(self, filter=None):
        try:
            if not filter:
                filter = {'id': self.entity.id}
            return self.session.query(self.entity.__class__).filter_by(**filter).first()
        except:
            self.session.rollback()
            traceback.print_exc(file=sys.stdout)
            Exception("Exception in method find from {0}".format(self))

    def update(self):
        if self.entity.id:
            entity = self.session.query(self.entity.__class__).filter_by(**{'id':self.entity.id}).update(
                self.entity._filter())#._Model__filter(
            self.session.commit()
            return entity
        else:
            raise Exception("{0} doesn't have id, cannot update".format(self.entity))

    def save(self):
        try:
            self.session.add(self.entity)
            self.session.commit()
        except:
            self.session.rollback()
            traceback.print_exc(file=sys.stdout)
            # print("Exception in {0} with entity {1} session {2}".format(self.entity, self.session))
            raise Exception("Exception in method save from {0}".format(self))

    def remove(self):
        if self.entity.id:
            # self.session.query(self.entity.__class__).filter_by(**{'id': self.entity.id}).delete()  # ._Model__filter(
            entity = self.find()
            if entity:
                # 'delete as cascade' ou use #cascade="all,delete" no relationship.
                self.session.delete(entity)
                self.session.commit()
        else:
            raise Exception("{0} doesn't have id, cannot update".format(self.entity))


class Model(object):
    def __init__(self, *args, **kwargs):
        raise Exception("Não é possível instanciar esse objeto.")

    def __setattr__(self, key, value):
        if key in ["id"] and self.__dict__ and self.__dict__.get(key):
            raise ValueError("Atributo constante.")
        super(Model, self).__setattr__(key, value)

    def __repr__(self):
        return "<{0}-(1)>".format(self.__class__, self.id)

    def __call__(self, session_object, *args, **kwargs):
        # assert isinstance(session_object, Banco)
        # assert isinstance(self, Base)
        return Handler(self, session_object)

    def _filter(self):
        __filter = self.__dict__.copy()
        aux = __filter.copy()
        for key, value in aux.items():
            if type(value) not in [str, int, float]:
                __filter.pop(key)
        # __filter.pop('_sa_instance_state')
        return __filter

    def __eq__(self, obj):
        return self.id == obj.id and self.__class__ == obj.__class__

    def __hash__(self):
        return self.id

class UsuarioPermissao(Base, Model):
    __tablename__ = "usuario_permissao"
    idUsuario = Column(Integer, ForeignKey("usuario.id"), primary_key=True)
    idPermissao = Column(Integer, ForeignKey("permissao.id"), primary_key=True)


#     usuario = relationship("Usuario", backref=backref("usuario_permissao"))
#     permissao = relationship("Permissao", backref=backref("usuario_permissao"))

# usuario_permissao = Table('usuario_permissao', Base.metadata,
#     Column('idUsuario', Integer, ForeignKey("usuario.id"), primary_key=True),
#     Column('idPermissao',Integer, ForeignKey("permissao.id"), primary_key=True)
# )
class UsuarioArquivo(Base, Model):
    __tablename__ = "usuario_arquivo"
    idUsuario = Column(Integer, ForeignKey("usuario.id"), primary_key=True)
    idArquivo = Column(Integer, ForeignKey("arquivo.id"), primary_key=True)

    # usuario = relationship("Usuario", backref="arquivo")
    # arquivo = relationship("Arquivo", backref="usuario")


class Usuario(Base, Model):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    login = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    email = Column(String, nullable=False)
    idAdm = Column(Integer, ForeignKey('usuario.id'))  # FOREIGN KEY(idAdm) references usuario(id)
    permissoes = relationship("Permissao", secondary="usuario_permissao", backref=backref("usuarios"),
                              collection_class=set)
    arquivos = relationship("Arquivo", secondary="usuario_arquivo", backref=backref("usuarios"))

    def __init__(self, *args, **kwargs):
        # self.__filter__ = kwargs
        # self._update = self.__dict__
        Base.__init__(self, *args, **kwargs)

    # adm = relationship("usuario", back_populates="usuario")

    def serialize(self):
        '''
        serialize serve para serealizar o obj, pode ser usado em sessão,
        diferente do atributo _filter(obs.: não use _filter, pois o mesmo contêm dados
        importantes e não deve estar contido na sessão devido a segurança.
        '''
        return {
            'login': self.login,
            'nome': self.nome,
            'email': self.email,
            'id': self.id
        }


class Arquivo(Base, Model):
    __tablename__ = "arquivo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nomeArquivo = Column(String, nullable=False)
    path = Column(String, nullable=False)
    tipoArquivo = Column(String, nullable=False)
    idPermissao = Column(Integer, ForeignKey("permissao.id"),
                         nullable=False)  # FOREIGN KEY(idPermissao) references permissao(id)
    arquivo_tags = relationship("ArquivoTags", back_populates="arquivo")
    permissao = relationship("Permissao", back_populates="arquivos")  # , uselist=True, collection_class=set)
    # arquivoTags = None

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nomeArquivo,
            'path': self.path,
            'tipo': self.tipoArquivo
        }

class ArquivoTags(Base, Model):
    __tablename__ = "arquivo_tags"
    idArquivo = Column(Integer, ForeignKey("arquivo.id"), primary_key=True, nullable=False)
    idTag = Column(Integer, primary_key=True, nullable=False)
    tag = Column(String, nullable=False)  # PRIMARY KEY(idArquivo, idTag)
    arquivo = relationship("Arquivo", back_populates="arquivo_tags")


class Permissao(Base, Model):
    __tablename__ = "permissao"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=True)
    descricao = Column(String, nullable=True)
    nivelRestricao = Column(Integer, nullable=False)
    arquivos = relationship("Arquivo", back_populates="permissao")

    # usuarios = relationship("Usuario", secondary=usuario_permissao)

    # arquivo = relationship("Arquivo", back_populates="permissao")


# Arquivo.arquivoTags = relationship("ArquivoTags", order_by=ArquivoTags.idArquivo, back_populates="arquivo")
# class UsuarioArquivo(Base):
#     idUsuario = Column(Integer, nullable=False)
#     idArquivo = Column(Integer, nullable=False)
#     # PRIMARY KEY(idUsuario, idArquivo),
#     # FOREIGN KEY(idUsuario) references usuario(id),
#     # FOREIGN KEY(idArquivo) references arquivo(id)
#


class DataBase(scoped_session):
    '''
    obs.: Talvez seja bom mudar os métodos para staticmethod ou classmethod

    irei trocar salvarUsuario por salvarUsuarios mais tarde.
                consultarUsuario por consultarUsuarios.

    '''

    def __init__(self, session_factory=None, *args, **kwargs):
        # self.bind = kwargs['engine']
        # if bind is None:
        #     bind = create_engine(bind_name, echo=echo)  # return the engine
        # elif bind is None and bind_name is None:
        #     raise AssertionError("bind parameter is None")
        #
        # kwargs["bind"] = bind
        kwargs['session_factory'] = session_factory
        super(DataBase, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<class '{0}' with id '{1}'>".format(self.__module__ + "." + self.__class__.__name__, id(self))

    def salvarUsuario(self, usuario):
        if isinstance(usuario, Usuario):
            # self.add(usuario)
            # self.commit()
            '''
            irei trocar salvarUsuario por salvarUsuarios mais tarde.
            '''
            usuario(self).save()
        else:
            raise TypeError("Objeto passado não é da instância Usuario")

    def consultarUsuario(self, usuario):
        if not isinstance(usuario, Usuario):
            raise TypeError("Objeto passado não é da instância Usuario")

        return usuario(self).find()

    def updateUsuario(self, usuario):
        if not isinstance(usuario, Usuario):
            raise TypeError("Objeto passado não é da instância Usuario")
        #
        # usuario2 = self.query(Usuario).filter_by(**usuario._filter).update(usuario._update, synchronize_session='evaluate')
        # self.commit()
        # stmt = update(Usuario).where(Usuario.id == 2). \
        #         values(nome='user #teste#')
        # self.execute(stmt)
        usuario(self).update()

    # def __call__(self, *args, **kwargs):
    #     # super(Banco, self).__call__(*args, **kwargs)
    #     Session.__call__(*args, **kwargs)


if __name__ == "__main__":
    pass
