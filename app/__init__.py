from flask import Flask
# object Flask from flask package
app = Flask(__name__)
# var app = instance of class Flask : Py predefined var to configure flask correctly
from app import routes
# app here is the package 
# routes module : URLs