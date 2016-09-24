"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWebProject import app
from . import createDB, User, engine, MACIDs
from passlib.hash import md5_crypt
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

@app.route('/create')
def create():
    createDB()
    return "True"

#assumes database is named Users
@app.route('/authenticate', methods=['POST'])
def authenticate(id):
    return json.dumps(md5_crypt.encrypt(datetime.utcnow().strftime('%m/%d/%Y')))

@app.route('/addDevice', methods=['POST'])
def addDevice(username, newMacID):
    session = Session()
    s = session.query(User).get(username)
    if not(s):
        return json.dumps('false')
    s.macids.append(MACIDs(macid = newMacID))
    session.commit()


"""def addFriend(username):
    s = Users.query.get(username)
    #friends = s.
    #i think we need a friends class in init to hold another table."""
