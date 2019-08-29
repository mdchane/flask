from datetime import datetime
from app import db, login
# import database instance
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
# db.Model is a base class for all models from Flask-SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # db.Column  class takes agr type + options
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    # access to all users posts, backref points back to user

    def __repr__(self):
        return '<User {}>'.format(self.username)
    # to print class objects

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # datetime.utcnow fct will be used
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # reference to id value from users table

    def __repr__(self):
        return '<Post {}>'.format(self.body)

@login.user_loader
# register user loader with flask-login 
def load_user(id):
    return User.query.get(int(id))