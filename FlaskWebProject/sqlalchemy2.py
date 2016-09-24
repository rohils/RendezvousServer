from flask import *
from sqlalchemy import *
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    friendsList = Column(list())


    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
        self.name, self.fullname, self.password)