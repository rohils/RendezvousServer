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

#returns api key based on hash of current datetime
@app.route('/authenticate', methods=['POST'])
def authenticate():
    return json.dumps(md5_crypt.encrypt(datetime.utcnow().strftime('%m/%d/%Y')))

@app.route('/addDevice', methods=['POST'])
def addDevice(username, newMacID):
    session = Session()
    s = session.query(User).get(username)
    if not(s):
        return json.dumps('false')
    s.macids.append(MACIDs(macid = newMacID))
    session.commit()


#username is the name of current user
#friend is gonna be a User object with all its attribuets (columns)
#return json of the friends database belonging to this current user.
@app.route('/addFriend', methods=['POST'])
def addFriend(username, friendname):
    session = Session()
    s = session.query(User).get(username)
    f = session.query(User).get(friendname)
    #dont know if below line works like this.
    s.friends.append(f)
    session.commit()
    return json.dumps(s.friends)


#username1 is name of guy who initiates friend request
#username 2 is name of person receiving friend request
#message is string, which is the message user1 sends to user 2
@app.route('/addReminder', methods=['POST'])
def addReminder(username1, username2, message):
    session = Session()
    s1 = session.query(User).get(username1)
    s2 = session.query(User).get(username2)
    newReminder = Reminder(id=md5_crypt.encrypt(username1+username2), userTrigger=s1,
        userReceiver=s2, reminderText=message, time=datetime.utcnow())
    session.add(newReminder)
    session.commit()
    return json.dumps(session.query(reminders).all())
