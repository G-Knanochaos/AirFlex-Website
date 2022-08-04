#database models stored here
from . import db
from flask_login import UserMixin

#class ACdata(db.Model):
'''
store progress (spending over time, KW over time) data, 
KwH, estimated bill, AC model, 
effeciency, BTU rating, location
AirCoin wallet - how much aircoin, how far below local average (watts)
'''

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #primary key is the main key for the user
    email = db.Column(db.String(100), unique=True) #
    password = db.Column(db.String(20))
    username = db.Column(db.String(50))
