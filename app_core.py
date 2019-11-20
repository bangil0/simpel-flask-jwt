""" App Core """

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

CONNECT = 'sqlite:////home/mumundira/Projects/belajar-python/flask-jwt/database/database.db'
app.config['SECRET_KEY'] = b'1\xbf+\xf78\xf0\x1c\xa7\xc0\xef\xa6\xfd2\xc0\x8a\x95\xce\xbc\xbaQW\x84\xd6\xce'
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
