from flask import Flask,render_template,request,redirect
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def create_app():
    # Initialize Flask application
    app = Flask(__name__, static_folder='scorm', template_folder='scorm')
    load_dotenv()
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token_cookie'  # Cookie name for storing the access token
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'  # Path for the cookie, default is '/'
    app.config['JWT_ACCESS_COOKIE_SAMESITE'] = 'Lax'  # SameSite attribute for the cookie (can be 'Lax', 'Strict', or 'None')
    app.config['JWT_ACCESS_COOKIE_SECURE'] = False  # Set to True if using HTTPS
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.config['JWT_ACCESS_CSRF_HEADER_NAME'] = 'X-CSRF-Token'  # CSRF header name
    app.config['JWT_ACCESS_CSRF_FIELD_NAME'] = 'csrf_token'  # CSRF field name
    app.config['JWT_CSRF_METHODS'] = ['POST', 'PUT', 'PATCH', 'DELETE']  # CSRF protected methods

    jwt = JWTManager(app)
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
    # Redirect to login page when unauthorized
        return redirect('/iauth/login')
    CORS(app, supports_credentials=True)
    return app


    
