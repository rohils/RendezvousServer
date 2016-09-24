"""
The flask application package.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from PasswordHash import PasswordHash as pwh

Base = declarative_base()
app = Flask(__name__)
db = SQLAlchemy(app)

class Password(db.TypeDecorator):
    impl = db.Text

    def __init__(self, **kwargs):
        super(Password, self).__init__(**kwargs)

    def process_bind_param(self, value, dialect):
        return self._convert(value).hash

    def process_result_value(self, value, dialect):
        if value is not None:
            return pwh(value)

    def validator(self, pwd):
        self._convert(pwd)

    def _convert(self, value):
        if type(value) == pwh:
            return value
        elif type(value) == str:
            return pwh.new(value)
        elif value is not None:
            raise TypeError('Cannot convert {} to a PasswordHash'.format(type(value)))

class MAC_IDs(db.model):
    __tablename__ = 'macids'
    id = db.Column(db.Integer, primary_key = True)
    macid = db.Column(db.String(128), unique = True)

class User(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    password = db.Column(Password)

    @validates('password')
    def _validate_password(self, key, pwd):
        return getattr(type(self) key).type.validator(pwd)





import FlaskWebProject.views
