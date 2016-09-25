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
import pickle
from PasswordHash import PasswordHash


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
            return PasswordHash.new(value)
        elif value is not None:
            raise TypeError('Cannot convert {} to a PasswordHash'.format(type(value)))


class APIKey(Base):
    __tablename__ = 'api_keys'

    apikey = db.Column(db.Text, primary_key= True)
    name = db.Column(db.String(80), db.ForeignKey('users.uname'))
    def __init__(self, apikey, name):
        self.apikey = apikey
        self.name = name

    def __repr__(self):
        return self.apikey

class MACIDs(Base):
    __tablename__ = 'mac_ids'

    macid = db.Column(db.String(128), primary_key = True)
    name = db.Column(db.String(80), db.ForeignKey('users.uname'))
    def __init__(self, macid, name):
        self.macid = macid
        self.name = name

    def __repr__(self):
        return '<MACID %r>' % self.macid

class User(Base):
    __tablename__ = 'users'
    uname = db.Column('uname', db.String(80), primary_key = True)
    pswd = db.Column('pswd', db.Text)
    friends = db.Column('friends', db.Text)
    macids = db.relationship('MACIDs')
    apikeys = db.relationship('APIKey')

    def __init__(self, uname, pswd, friends):
        self.uname = uname
        self.pswd = pswd
        self.friends = friends

    def __repr__(self):
        return '<User %r>' % self.uname


class Reminder(Base):
    __tablename__ = 'reminders'
    id = db.Column('id', db.Integer, primary_key = True)
    userTrigger = db.Column('utrigger', db.String(80))
    userReceiver = db.Column('ureceiver', db.String(80))
    reminderText = db.Column('message', db.Text)
    time = db.Column('datetime', db.Integer)

    def __init__(self, userTrigger, userReceiver, reminderText, time):
        self.userTrigger = userTrigger
        self.userReceiver = userReceiver
        self.reminderText = reminderText
        self.time = time

    def __repr__(self):
        return '<Reminder>'


DB_CONN_URI_DEFAULT = "./rendezvousdb.db"
conn = sqlite3.connect(DB_CONN_URI_DEFAULT)
engine = create_engine("sqlite:///" + DB_CONN_URI_DEFAULT)
Base.metadata.create_all(engine)

def createDB():
    DB_CONN_URI_DEFAULT = "./rendezvousdb.db"
    engine = create_engine("sqlite:///" + DB_CONN_URI_DEFAULT)
    Base.metadata.create_all(engine)





import FlaskWebProject.views
