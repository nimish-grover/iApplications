from dotenv import load_dotenv
from flask import Flask,redirect
from flask_migrate import Migrate
from iAuth.app.routes.index import blp as indexBlueprint
from .db import db
from flask_smorest import Api
from flask_login import LoginManager
from iAuth.app.models.user import UserModel
from flask_jwt_extended import JWTManager
from iAuth.app.routes.auth import blp as AdminBlueprint
from iAuth.app.models.inrole import inRoleModel
from iAuth.app.models.roles import RolesModel
from iAuth.app.models.user import UserModel
import os
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config['SECRET_KEY']='b5e4e6b5b74e9fc20b477ebe62bed84188daf2a581a793d61c2c61ac7cee68a0'
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token_cookie'  # Cookie name for storing the access token
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'  # Path for the cookie, default is '/'
    app.config['JWT_ACCESS_COOKIE_SAMESITE'] = 'Lax'  # SameSite attribute for the cookie (can be 'Lax', 'Strict', or 'None')
    app.config['JWT_ACCESS_COOKIE_SECURE'] = False  # Set to True if using HTTPS
    app.config['JWT_ACCESS_CSRF_HEADER_NAME'] = 'X-CSRF-Token'  # CSRF header name
    app.config['JWT_ACCESS_CSRF_FIELD_NAME'] = 'csrf_token'  # CSRF field name
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.config['JWT_CSRF_METHODS'] = ['POST', 'PUT', 'PATCH', 'DELETE']  # CSRF protected methods

    app.config['API_TITLE']='iauth'
    app.config['API_VERSION']='v1'
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_DATABASE_URI']= os.getenv('AUTH_DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS']=True

    login_manager = LoginManager()  # Initializing LoginManager
    login_manager.login_view = 'admin.login'  # Setting the login view
    login_manager.init_app(app)  # Initializing LoginManager with the Flask app
    jwt = JWTManager(app)
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
    # Redirect to login page when unauthorized
        return redirect('/iauth/login')
    
    
    CORS(app, supports_credentials=True)
    @login_manager.user_loader
    def load_user(user_id):
        return UserModel.query.get(int(user_id))
    
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    api.register_blueprint(indexBlueprint)
    api.register_blueprint(AdminBlueprint)
    
    return app