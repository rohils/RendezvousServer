"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWebProject import app
from . import createDB
from passlib.hash import md5_crypt

@app.route('/create')
def create():
    createDB()
    return "True"

#assumes database is named Users
@app.route('/authenticate', methods=['POST'])
def authenticate(id):
    #s = Users.query.get(id)
    #toHash = s.password._convert(s.username)

    d = datetime.utcnow()
    d = d.strftime('%m/%d/%Y')
    
    #cirque du twerque of all api key generations
    return json.dumps(md5_crypt.encrypt(d))

@app.route('/addDevice', methods=['POST'])
def addDevice(username, newMacID):
    s = Users.query.get(username)
    mac = s.macids
    apiKey = s.apiKey

    if apiKey == s.password._convert(s.username):
        s.macids = s.macids.append
        db.sessions.commit()
        return true
    else: return false

"""def addFriend(username):
    s = Users.query.get(username)
    #friends = s.
    #i think we need a friends class in init to hold another table."""