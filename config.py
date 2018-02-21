import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nigdy-nie-zgadniesz'
    # SERVER_NAME = "0.0.0.0:5467"
