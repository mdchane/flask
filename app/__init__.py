from flask import Flask
# object Flask from flask package
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
# var app = instance of class Flask : Py predefined var to configure flask correctly
app.config.from_object(Config)
# apply config.py
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
#to redirect to login page

from app import routes, models
# app here is the package 
# routes module : URLs