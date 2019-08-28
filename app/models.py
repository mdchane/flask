from datetime import datetime
from app import db
# import database instance

class User(db.Model):
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

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # datetime.utcnow fct will be used
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # reference to id value from users table

    def __repr__(self):
        return '<Post {}>'.format(self.body)