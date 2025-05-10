import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'changeme')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///../instance/evently.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
