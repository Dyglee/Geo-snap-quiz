import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Meriem60641939'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://geosnap_user:Meriem60641939@localhost/geosnap_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False