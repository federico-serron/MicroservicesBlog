from unicodedata import name
from config import db
from flask_login import UserMixin


class Users(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    country = db.Column(db.String(25), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(32), nullable = False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    role_id = db.Column(db.Integer, default=2)

    def __init__(self,name, country, age, email, username, password, role_id):
        self.name = name
        self.country = country
        self.age = age
        self.email = email
        self.username = username
        self.password = password
        self.role_id = role_id
        