import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Meriem60641939'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///geosnap.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False