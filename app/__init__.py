from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_migrate import Migrate

# Init Plugins
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app(config_class=Config):
    #Init the app
    app = Flask(__name__)
    app.static_folder = "./static"
    #Link in the Config (using config_class allows swapping configs depending on environment)
    app.config.from_object(config_class)
    
    #Register plugins
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    login.login_view = 'auth.login'
    login.login_message = 'Please login to view this page'
    login.login_message_category = 'warning'

    from .blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    return app