"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWebProject import app
from . import createDB, User, engine, MACIDs, Password, APIKey, Reminder
from passlib.hash import md5_crypt
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

@app.route('/create')
def create():
    return createDB()

#returns api key based on hash of current datetime
@app.route('/authenticate', methods=['POST','GET'])
def authenticate(username, password):
    session = Session()
    s = session.query(User).get(username)
    if s.password == password:
        apiKey = md5_crypt.encrypt(datetime.utcnow().strftime('%m/%d/%Y'))
        session.add(APIKey(apikey = apiKey))
        session.commit()
        return json.dumps(apiKey)
    return json.dumps(False)


@app.route('/addDevice', methods=['POST','GET'])
def addDevice(username, newMacID):
    session = Session()
    s = session.query(User).get(username)
    if not(s):
        return json.dumps(False)
    s.macids.append(MACIDs(macid = newMacID))
    session.commit()
    return json.dumps(True)


#username is the name of current user
#friend is gonna be a User object with all its attribuets (columns)
#return json of the friends database belonging to this current user.

@app.route('/addFriend', methods=['POST','GET'])]
def addFriend(username, friendname):
    session = Session()
    s = session.query(User).get(username)
    if not(s):
        return json.dumps(False)
    f = session.query(User).get(friendname)
    if not(f):
        return json.dumps(False)
    #dont know if below line works like this.
    s.friends.append(f)
    session.commit()
    return json.dumps(True)


#username1 is name of guy who initiates friend request
#username 2 is name of person receiving friend request
#message is string, which is the message user1 sends to user 2
@app.route('/addReminder', methods=['POST','GET'])
def addReminder(username1, username2, message):
    session = Session()
    s1 = session.query(User).get(username1)
    if not(s1):
        return json.dumps(False)
    s2 = session.query(User).get(username2)
    if not(s2):
        return json.dumps(False)
    newReminder = Reminder(userTrigger=s1, userReceiver=s2, reminderText=message, time=datetime.utcnow())
    session.add(newReminder)
    session.commit()
    return json.dumps(True)

@app.route('/friendsList', methods=['POST','GET'])
def friendsList(username):
    session = Session()
    s = session.query(User).get(username)
    return json.dumps(s.friends)

@app.route('/reminderList', methods=['POST','GET'])
def reminderList():
    session = Session()
    s = session.query(Reminder).all()
    return json.dumps(s)
