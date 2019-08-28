from flask import Flask
# object Flask from flask package
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
# var app = instance of class Flask : Py predefined var to configure flask correctly
app.config.from_object(Config)
# apply config.py
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
# app here is the package 
# routes module : URLs