"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWebProject import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

@app.route('/create')
def create():
    DB_CONFIG_DICT = {
        'user': 'renDEVous',
        'password': 'qwerty232',
        'host': 'rendezvousserver.azurewebsites.net',
        'port': 443,
    }
    DB_CONN_FORMAT = "postgresql://{user}:{password}@{host}:{port}/{database}"
    DB_CONN_URI_DEFAULT = (DB_CONN_FORMAT.format(database='rendezvousDB',**DB_CONFIG_DICT))
    engine = create_engine(DB_CONN_URI_DEFAULT)
    if not database_exists(engine.url):
        create_database(engine.url)
    print(database_exists(engine.url))
    return DB_CONN_URI_DEFAULT
