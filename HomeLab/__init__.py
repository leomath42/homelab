from .model import DataBase
from .config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask
import os

# cria uma scoped session com DataBase
engine = create_engine(config['engine_name'])
session_factory = sessionmaker(bind=engine)
database = DataBase(session_factory)

# Flask app
app = Flask(__name__)
app.secret_key = os.urandom(16)

from HomeLab.routes import *

# app.config["APPLICATION_ROOT"] = "/home/mohelot/projetos/home_lab/"
__all__ = ['model', 'config', 'controller', 'util']
__version__ = 'v0.1.2'
__author__ = "leomath42"
