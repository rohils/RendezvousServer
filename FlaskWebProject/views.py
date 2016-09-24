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

#returns api key based on hash of current datetime
@app.route('/authenticate', methods=['POST'])
def authenticate(id):
    return json.dumps(md5_crypt.encrypt(datetime.utcnow().strftime('%m/%d/%Y')))

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

#username is the name of current user
#friend is gonna be a User object with all its attribuets (columns)
#return json of the friends database belonging to this current user.
@app.route('/addFriend', methods=['POST'])
def addFriend(username, friend):
    s = Users.query.get(username)
    #dont know if below line works like this.
    s.friends.append(friend)
    db.sessions.commit()
    return json.dumps(s.friends)


    
