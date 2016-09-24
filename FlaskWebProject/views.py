"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from FlaskWebProject import app

@app.route('/create')

#assumes database is named Users
@app.route('/authenticate', methods=['POST'])
def authenticate(id):
    s = Users.query.get(id)
    toHash = s.password._convert(s.username)
    #cirque du twerque of all api key generations
    return json.dumps(toHash)

@app.route('/addDevice', methods=['POST'])
def addDevice(username, newMacID):
    s = Users.query.get(username)
    mac = s.macids
    apiKey = s.apiKey

    if apiKey == s.password._convert(s.username):
        mac.append(newMacID)
        db.sessions.commit()
        return true
    else: return false