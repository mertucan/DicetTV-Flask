from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True)

class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    message = db.Column(db.String(256), index=True)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    package = db.Column(db.String(64), index=True)
    price = db.Column(db.String(64), index=True)
    month = db.Column(db.String(64), index=True)
    desc = db.Column(db.String(64), index=True)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    price = db.Column(db.String(64), index=True)
