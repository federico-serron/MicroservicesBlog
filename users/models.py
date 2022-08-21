from config import db
from flask_login import UserMixin


class Users(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(20))

    def __init__(self, username, password):
        self.username = username
        self.password = password