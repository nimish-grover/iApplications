
from flask import Flask
from iLand.app.db import db
from flask_migrate import Migrate
from iLand.app.routes.state_wise_area import blp as StateBlueprint


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='b5e4e6b5b74e9fc20b477ebe62bed84188daf2a581a793d61c2c61ac7cee68a0'
    app.config['API_TITLE']='iland'
    app.config['API_VERSION']='v1'
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_DATABASE_URI']= "postgresql://postgres.qyjsobeykjepsmnuujfh:IZmLkOy4xXA05UQA@aws-0-us-west-1.pooler.supabase.com:5432/postgres"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS']=True


    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(StateBlueprint)

    return app