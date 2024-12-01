from flask import Flask,render_template,request,redirect
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import redis
from flask_session import Session

def create_app():
    # Initialize Flask application
    app = Flask(__name__, static_folder='scorm', template_folder='scorm')
    load_dotenv()
    CORS(app)
    return app


    
