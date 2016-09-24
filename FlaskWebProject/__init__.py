"""
The flask application package.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import validates
from sqlalchemy import create_engine
import sqlite3

Base = declarative_base()
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Password(db.TypeDecorator):
    impl = db.Text

    def __init__(self, **kwargs):
        super(Password, self).__init__(**kwargs)

    def process_bind_param(self, value, dialect):
        return self._convert(value).hash

    def process_result_value(self, value, dialect):
        if value is not None:
            return PasswordHash(value)

    def validator(self, pwd):
        self._convert(pwd)

    def _convert(self, value):
        if type(value) == PasswordHash:
            return value
        elif type(value) == str:
            return pwh.new(value)
        elif value is not None:
            raise TypeError('Cannot convert {} to a PasswordHash'.format(type(value)))

class APIKey(Base):
    __tablename__ = 'apikeys'

    id = db.Column(db.Integer, primary_key = True)
    apikey = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class MACIDs(Base):
    __tablename__ = 'macids'

    id = db.Column(db.Integer, primary_key = True)
    macid = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class User(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column('username', db.String(80), unique = True)
    password = db.Column('password', Password)
    @validates('password')
    def _validate_password(self, key, pwd):
        return getattr(type(self), key).type.validator(pwd)
    friends = db.relationship('User')
    macids = db.relationship('MACIDs')
    apikeys = db.relationship('APIKey')

class Reminder(Base):
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key = True)
    userTrigger = db.relationship('User', backref= 'reminders', lazy='dynamic', uselist = False)
    userReceiver = db.relationship('User', backref= 'reminders', lazy='dynamic', uselist = False)
    reminderText = db.Column('message', db.Text)
    time = db.Column('time', db.DateTime, primary_key = True)

DB_CONN_URI_DEFAULT = "./rendezvousdb.db"
conn = sqlite3.connect(DB_CONN_URI_DEFAULT)
engine = create_engine("sqlite:///" + DB_CONN_URI_DEFAULT)
Base.metadata.create_all(engine)

def createDB():
    DB_CONN_URI_DEFAULT = "./rendezvousdb.db"
    conn = sqlite3.connect(DB_CONN_URI_DEFAULT)
    engine = create_engine("sqlite:///" + DB_CONN_URI_DEFAULT)
    Base.metadata.create_all(engine)





import FlaskWebProject.views
