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
    createDB()
    return "True"


@app.route('/register/<username>/<password>', methods=['POST','GET'])
def register(username, password):
    session = Session()
    s = session.query(User).get(username)
    if not(s):
        session.add(User(username = username, password = password))
        session.flush()
        session.close()
        return({"success":True})
    else:
        return({"success":False})


#returns api key based on hash of current datetime
@app.route('/authenticate/<username>/<password>', methods=['POST','GET'])
def authenticate(username, password):
    session = Session()
    s = session.query(User).get(username)
    if s.password == password:
        apiKey = md5_crypt.encrypt(datetime.utcnow().strftime('%m/%d/%Y'))
        session.add(APIKey(apikey = apiKey))
        session.flush()
        session.close()
        return json.dumps({"success":True, "apiKey":apiKey})
    return json.dumps({"success":False})


@app.route('/addDevice/<username>/<apiKey>/<newMacID>', methods=['POST','GET'])
def addDevice(username, apiKey, newMacID):
    session = Session()
    s = session.query(User).get(username)
    if not(s):
        session.close()
        return json.dumps({"success":False})
    if apiKey not in session.query(APIKey).filter(user_id == s.id).all():
        session.close()
        return json.dumps({"success":False})
    s.macids.append(MACIDs(macid = newMacID))
    session.flush()
    session.close()
    return json.dumps({"success":True})


#username is the name of current user
#friend is gonna be a User object with all its attribuets (columns)
#return json of the friends database belonging to this current user.

@app.route('/addFriend/<username>/<apiKey>/<friendName>', methods=['POST','GET'])
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
    if apiKey not in session.query(APIKey).filter(user_id == s.id).all():
        session.close()
        return json.dumps({"success":False})
    #dont know if below line works like this.
    s.friends.append(f)
    session.flush()
    session.close()
    return json.dumps({"success":True})


#username1 is name of guy who initiates friend request
#username 2 is name of person receiving friend request
#message is string, which is the message user1 sends to user 2
@app.route('/addReminder/<apiKey>/<userReceiver>/<userTrigger>/<message>/<time>', methods=['POST','GET'])
def addReminder(apiKey, userReceiver, userTrigger, message, time):
    session = Session()
    s1 = session.query(User).get(userReceiver)
    if not(s1):
        session.close()
        return json.dumps({"success":False})
    s2 = session.query(User).get(userTrigger)
    if not(s2):
        session.close()
        return json.dumps({"success":False})
    if apiKey not in session.query(APIKey).filter(user_id == s1.id).all():
        session.close()
        return json.dumps({"success":False})
    newReminder = Reminder(userTrigger=s2, userReceiver=s1, reminderText=message, time=time)
    session.add(newReminder)
    session.flush()
    session.close()
    return json.dumps({"success":True})

@app.route('/friendsList/<username>/<apiKey>', methods=['POST','GET'])
def friendList(username, apiKey):
    session = Session()
    s = session.query(User).get(username)
    if not(s):
        session.close()
        return json.dumps({"success":False})
    if apiKey not in session.query(APIKey).filter(user_id == s.id).all():
        session.close()
        return json.dumps({"success":False})
    session.close()
    return json.dumps({"users":s.friends, "success":True})

@app.route('/reminderList/<username>/<apiKey>', methods=['POST','GET'])
def reminderList(username, apiKey):
    session = Session()
    s = session.query(Reminder).filter(Reminder.userReceiver.username==username).all()
    if not(s):
        session.close()
        return json.dumps({"success":False})
    if apiKey not in session.query(APIKey).filter(user_id == s.id).all():
        session.close()
        return json.dumps({"success":False})
    session.close()
    return json.dumps({"reminders":s, "success":True})

@app.route('/processIds/<idList>/<username>/<apiKey>', methods=['POST','GET'])
def processIds(idList, username, APIKey):
    session = Session()
    s = session.query(Reminder).filter(Reminder.userReceiver.username==username).all()
    if apiKey not in session.query(APIKey).filter(user_id == s.id).all():
        session.close()
        return json.dumps({"success":False})
    answerList = []
    for hash in idList:
        m = session.query(MACIDS).get(hash).first().user_id
        user = session.query(Users).get(m).first()
        if not user: answerList.append("")
        else: answerList.append(user.username)
    session.close()
    return json.dumps({"userList":answerList,"success":True})

@app.route('/changePassword/<username>/<oldPassword>/<newPassword>', methods=['POST','GET'])
def changePassword(username, oldPassword, newPassword):
    session = Session()
    s = session.query(User).get(oldPassword).first()
    t = session.query(User).get(username).first()
    if not s or not t or not s == t: return json.dumps({"success":False})
    s.password = newPassword
    session.commit()
    return json.dumps({"success":True})

@app.route('/userExists', methods=['POST','GET'])
def userExists(userQuery, username, apiKey):
    session = Session()
    s = session.query(Users).get(userQuery).all()
    if apiKey not in session.query(APIKey).filter(user_id == s.id).all():
        session.close()
        return json.dumps({"success":False})
    else: return json.dumps({"success":True if s else False})
