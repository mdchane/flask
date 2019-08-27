import os

# config settings as class var in Config class
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
# secret key against CSRF attack