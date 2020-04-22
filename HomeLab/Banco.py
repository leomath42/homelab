#!/usr/bin/python3
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, Session


import sys
import os

engine = create_engine("sqlite:////home/mohelot/projetos/home_lab/bancos/homelab.db", echo=True)
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    login = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    email = Column(String, nullable=False)
    idAdm = Column(Integer, ForeignKey('usuario.id')) # FOREIGN KEY(idAdm) references usuario(id)
    # adm = relationship("usuario", back_populates="usuario")




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
        return self.query(Usuario).filter_by(login=usuario.login).all()

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
    b = Banco(engine)
    print(b.query(Arquivo).all())
    print(b)