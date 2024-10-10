from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from app.extensions import db
from app.routes import main_routes
from app.models.user import User
from config import Config

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'main_routes.login'  # Redirects to login page if not authenticated

    # Register blueprints
    app.register_blueprint(main_routes)

    return app

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
