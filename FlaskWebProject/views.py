"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWebProject import app
from . import createDB, User, engine, MACIDs, Password, APIKey, Reminder, db
import sqlite3
import hashlib
import uuid
from sqlalchemy.orm import sessionmaker
import pickle
from PasswordHash import PasswordHash
import json

def hash_api(text):
    salt = uuid.uuid4().hex
    return hashlib.md5(salt.encode() + text.encode()).hexdigest()

def hash_text(text):
    salt = uuid.uuid4().hex
    return hashlib.md5(salt.encode() + text.encode()).hexdigest() + ":" + salt

def check_hash(hashed_text, input_text):
    text, salt = hashed_text.split(':')
    return text == hashlib.md5(salt.encode() + input_text.encode()).hexdigest()

Session = sessionmaker(bind = engine)

@app.route('/create')
def create():
    createDB()
    return "True"


@app.route('/register/<username>/<password>/', methods=['GET','POST'])
def register(username, password):
    session = Session()
    s = session.query(User).get(username)
    if not(s):
        new = User(uname = username, pswd = hash_text(password), friends = '')
        session.add(new)
        session.commit()
        session.close()
        return json.dumps({"success":True})
    else:
        return json.dumps({"success":False})


#returns api key based on hash of current datetime
@app.route('/authenticate/<username>/<password>/', methods=['GET','POST'])
def authenticate(username, password):
    session = Session()
    s = session.query(User).get(username)
    if not(s):
        return json.dumps({"success":False})
    if check_hash(s.pswd, password):
        apiKey = hash_api(datetime.utcnow().strftime('%m/%d/%Y'))
        session.add(APIKey(apikey = apiKey, name = s.uname))
        session.commit()
        session.close()
        return json.dumps({"success":True, "apiKey":apiKey})
    return json.dumps({"success":False})


@app.route('/addDevice/<username>/<path:apiKey>/<newMacID>/', methods=['POST','GET'])
def addDevice(username, apiKey, newMacID):
    session = Session()
    s = session.query(User).get(username)
    if not(s):
        session.close()
        return json.dumps({"success":False})
    if apiKey not in [str(i) for i in session.query(APIKey).filter(APIKey.name == s.uname).all()]:
        session.close()
        return json.dumps({"success":False})
    s.macids.append(MACIDs(macid = newMacID, name = s.uname))
    session.commit()
    session.close()
    return json.dumps({"success":True})


#username is the name of current user
#friend is gonna be a User object with all its attribuets (columns)
#return json of the friends database belonging to this current user.

@app.route('/addFriend/<username>/<path:apiKey>/<friendName>/', methods=['POST','GET'])
def addFriend(username, apiKey, friendName):
    session = Session()
    s = session.query(User).get(username)
    if not(s):
        session.close()
        return json.dumps({"success":False})
    f = session.query(User).get(friendName)
    if not(f):
        session.close()
        return json.dumps({"success":False})
    if apiKey not in [str(i) for i in session.query(APIKey).filter(APIKey.name == s.uname).all()]:
        session.close()
        return json.dumps({"success":False})
    if s.friends == "":
        s.friends = friendName
    else:
        fnames = s.friends.split(',')
        if friendName in fnames:
            session.close()
            return json.dumps({"success":False})
        s.friends = s.friends + "," + friendName
    session.commit()
    session.close()
    return json.dumps({"success":True})


#username1 is name of guy who initiates friend request
#username 2 is name of person receiving friend request
#message is string, which is the message user1 sends to user 2
@app.route('/addReminder/<path:apiKey>/<userReceiver>/<userTrigger>/<message>/', methods=['POST','GET'])
def addReminder(apiKey, userReceiver, userTrigger, message):
    session = Session()
    s1 = session.query(User).get(userReceiver)
    if not(s1):
        session.close()
        return json.dumps({"success":False})
    s2 = session.query(User).get(userTrigger)
    if not(s2):
        session.close()
        return json.dumps({"success":False})
    if apiKey not in [str(i) for i in session.query(APIKey).filter(APIKey.name == s1.uname).all()]:
        session.close()
        return json.dumps({"success":False})
    newReminder = Reminder(userTrigger=userTrigger, userReceiver=userReceiver, reminderText=message, time=0)
    session.add(newReminder)
    session.commit()
    session.close()
    return json.dumps({"success":True})

@app.route('/friendList/<username>/<path:apiKey>/', methods=['POST','GET'])
def friendList(username, apiKey):
    session = Session()
    s = session.query(User).get(username)
    if not(s):
        session.close()
        return json.dumps({"success":False})
    if apiKey not in [str(i) for i in session.query(APIKey).filter(APIKey.name == s.uname).all()]:
        session.close()
        return json.dumps({"success":False})
    fnames = s.friends.split(',')
    session.close()
    return json.dumps({"users":fnames, "success":True})

@app.route('/reminderList/<username>/<path:apiKey>/', methods=['POST','GET'])
def reminderList(username, apiKey):
    session = Session()
    s = session.query(User).get(username)
    r = session.query(Reminder).filter(Reminder.userReceiver==username).all()
    session.commit()
    rs = []
    for reminders in r:
        rs.append([reminders.id, reminders.userReceiver, reminders.userTrigger, reminders.reminderText, reminders.time])
    if not(s):
        session.close()
        return json.dumps({"success":False})
    if apiKey not in [str(i) for i in session.query(APIKey).filter(APIKey.name == s.uname).all()]:
        session.close()
        return json.dumps({"success":False})
    session.close()
    return json.dumps({"reminders":rs, "success":True})

@app.route('/processIds/<idList>/<username>/<path:apiKey>/', methods=['POST','GET'])
def processIds(idList, username, apiKey):
    session = Session()
    s = session.query(User).get(username)
    p = session.query(Reminder).filter(Reminder.userReceiver==username).all()
    if apiKey not in [str(i) for i in session.query(APIKey).filter(APIKey.name == username).all()]:
        session.close()
        return json.dumps({"success":False})
    answerList = []
    ids = idList.split(',')
    print(ids)
    for hash in ids:
        m = session.query(MACIDs).get(hash)
        if not(m):
            answerList.append("")
        else:
            answerList.append(m.name)
    session.close()
    return json.dumps({"userList":answerList,"success":True})

@app.route('/changePassword/<username>/<oldPassword>/<newPassword>/', methods=['POST','GET'])
def changePassword(username, oldPassword, newPassword):
    session = Session()
    s = session.query(User).get(username)
    op = s.pswd
    try:
        if s and check_hash(op, oldPassword):
            s.pswd = hash_text(newPassword)
            session.commit()
            session.close()
            return json.dumps({"success":True})
        else:
            session.close()
            return json.dumps({"success":False})
    except:
        session.close()
        return json.dumps({"success":False})
    session.close()
    return json.dumps({"success":False})

@app.route('/userExists/<userQuery>/<username>/<path:apiKey>/', methods=['POST','GET'])
def userExists(userQuery, username, apiKey):
    session = Session()
    a = session.query(User).get(username)
    s = session.query(User).get(userQuery)
    session.commit()
    if apiKey not in [str(i) for i in session.query(APIKey).filter(APIKey.name == a.uname).all()]:
        session.close()
        return json.dumps({"success":False})
    else:
        session.close()
        return json.dumps({"success":True if s else False})

@app.route('/setReminderTime/<username>/<path:apiKey>/<id>/<time>', methods=['POST','GET'])
def setReminderTime(username, apiKey, id, time):
    session = Session()
    s = session.query(User).get(username)
    if not(s):
        session.close()
        return json.dumps({"success":False})
    if apiKey not in [str(i) for i in session.query(APIKey).filter(APIKey.name == s.uname).all()]:
        session.close()
        return json.dumps({"success":False})
    r = session.query(Reminder).get(id)
    if not(r):
        session.close()
        return json.dumps({"success":False})
    r.time = time
    session.commit()
    session.close()
    return json.dumps({"success":True})
