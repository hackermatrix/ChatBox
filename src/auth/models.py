from src import bcrypt,db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String,nullable=False,unique=True)
    username = db.Column(db.String,nullable=False,unique=True)
    password = db.Column(db.String,nullable=False)
    created_on = db.Column(db.DateTime,nullable=False)

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()

    def __repr__(self):
        return f"username : {self.username}"

