import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from iJalagam.app.db import db
from iJalagam.app.models import State, District, Block, Village
from iJalagam.app.models.users import User
from iJalagam.app.routes.auth import blp as authBlueprint
from iJalagam.app.routes.routes import blp as routesBlueprint
from iJalagam.app.routes.entries import blp as entryBlueprint
from iJalagam.app.routes.mobile import blp as mobileBlueprint

def create_app():
    app = Flask(__name__)
    load_dotenv()
    
    # configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("JALAGAM_DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # or 'Lax' or 'Strict'
    app.config['SESSION_COOKIE_SECURE'] = True  # Required if SameSite=None
    app.config['SECRET_KEY']=os.getenv("JALAGAM_SECRET_KEY")

    # register db
    db.init_app(app)
    current_directory = os.getcwd()
    migrations_directory = current_directory + '/iJalagam/migrations'
    migrate = Migrate(app, db, directory=migrations_directory)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    # register blueprints
    app.register_blueprint(authBlueprint )
    app.register_blueprint(routesBlueprint)
    app.register_blueprint(entryBlueprint, url_prefix='/data')
    app.register_blueprint(mobileBlueprint, url_prefix='/m')
    return app