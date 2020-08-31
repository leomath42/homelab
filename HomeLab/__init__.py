from .model import DataBase
from .config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask
import os
import json

# cria uma scoped session com DataBase
engine = create_engine(config['engine_name'])
session_factory = sessionmaker(bind=engine)
database = DataBase(session_factory)

# Flask app
app = Flask(__name__)
app.secret_key = os.urandom(16)
app.config['UPLOAD_FOLDER'] = "/data"
# UPLOAD_FOLDER = '/path/to/the/uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config["APPLICATION_ROOT"] = "/home/mohelot/projetos/home_lab/"

from HomeLab.routes import *

__all__ = ['model', 'config', 'controller', 'util']
__version__ = 'v0.1.2'
__author__ = "leomath42"
