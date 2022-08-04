#database models stored here
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class ACdatum(db.Model):
    id = db.Column(db.Integer, primary_key=True) #main key that will be used to identify any saved ACdata instances
    hours = db.Column(db.Integer())
    temp = db.Column(db.Integer())
    estimated_bill = db.Column(db.Integer())
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #func.now() returns current date and time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #connects ACdata to a user

''' 
store progress (spending over time, KW over time) data, 
KwH, estimated bill, AC model, 
effeciency, BTU rating, location
AirCoin wallet - how much aircoin, how far below local average (watts)
'''

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #primary key is the main key for the user
    email = db.Column(db.String(100), unique=True) 
    password = db.Column(db.String(20))
    username = db.Column(db.String(50), unique=True)
    ACdata = db.relationship('ACdatum') #reference to ACdatum from User #ACdata is list of ACdatum
