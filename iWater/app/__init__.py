from datetime import timedelta
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager
from iWater.app.db import db
from iWater.app.routes.auth import blp as UserBlueprint
from iWater.app.routes.controllers import blp as controllerBlueprint
from iWater.app.routes.pwa import blp as pwaBlueprint
from iWater.app.routes.waterbody_routes import blp as wbBlueprint
from iWater.app.routes.wb_api import blp as wbApiBlueprint
from iWater.app.routes.entry import blp as EntryBlueprint
from iWater.app.routes.village_water_budget import blp as VillageBudget
from iWater.app.models.water_bodies_mp import Water_bodies_mp
from iWater.app.models.user import UserModel
from iWater.app.models.inrole import inRoleModel
from iWater.app.models.roles import RolesModel
from flask_login import current_user


def create_app():
    app = Flask(__name__)
    load_dotenv()

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("WATER_DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY']=os.getenv("WATER_SECRET_KEY")
    app.config['JWT_SECRET_KEY']=os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=180)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=120)

    # SWAGGER UI
    app.config['API_TITLE']='iWater'
    app.config['API_VERSION']='v1'
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    login_manager = LoginManager()  # Initializing LoginManager
    login_manager.login_view = 'admin.login'  # Setting the login view
    login_manager.init_app(app)  # Initializing LoginManager with the Flask app

    @login_manager.user_loader
    def load_user(user_id):
        return UserModel.query.get(int(user_id))
    
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    api = Api(app)
    jwt = JWTManager(app)

    # @app.context_processor
    # def inject_user_type():
    #     if current_user.is_authenticated:
    #         id = current_user.id
    #         check_admin = inRoleModel.get_role_by_id(id)
    #         if str(check_admin).lower() != 'user':
    #             admin_control = True
    #         else:
    #             admin_control = False
    #     else:
    #         admin_control = False
            
    # register blueprints
     # Register Blueprints
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(pwaBlueprint)
    api.register_blueprint(controllerBlueprint)
    api.register_blueprint(wbBlueprint, url_prefix='/wb')
    api.register_blueprint(wbApiBlueprint, url_prefix='/wb/api')
    api.register_blueprint(VillageBudget)
    api.register_blueprint(EntryBlueprint)


    return app