from config import db
from flask_login import UserMixin

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(50), nullable=True)
    status = db.Column(db.Integer, default=2)
    author = db.Column(db.String(20), nullable = False)
    date = db.Column(db.Date)
    
    def __init__(self, title, description, image_url, status, author, date):
        self.title = title
        self.description = description
        self.image_url = image_url
        self.status = status
        self.author = author
        self.date = date
        