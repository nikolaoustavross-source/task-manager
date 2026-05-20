from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'changeme')
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{os.environ.get('DB_USER', 'taskuser')}:"
        f"{os.environ.get('DB_PASSWORD', 'taskpass')}@"
        f"{os.environ.get('DB_HOST', 'db')}/"
        f"{os.environ.get('DB_NAME', 'taskdb')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes.auth import auth_bp
    from .routes.tasks import tasks_bp
    from .routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app
