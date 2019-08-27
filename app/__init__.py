from flask import Flask
# object Flask from flask package
from config import Config

app = Flask(__name__)
# var app = instance of class Flask : Py predefined var to configure flask correctly
app.config.from_object(Config)
# apply config.py

from app import routes
# app here is the package 
# routes module : URLs