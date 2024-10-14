import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'fallback_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://geosnap_db_user:DyceFrJwCxTBM2vaoItpdV6xgIo3aqGR@dpg-cs6lcglsvqrc73f5sap0-a.oregon-postgres.render.com/geosnap_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_PERMANENT = False