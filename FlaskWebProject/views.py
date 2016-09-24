"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWebProject import app
from . import createDB

@app.route('/create')
def create():
    createDB()
    return "True"
