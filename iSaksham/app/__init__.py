from http.client import HTTPException
from logging.handlers import RotatingFileHandler
import os
import traceback
import logging
from flask import Flask, g, render_template, request, session,url_for,redirect  # Importing necessary Flask modules
from iSaksham.app.db import db  # Importing database extension
from flask_migrate import Migrate  # Importing Flask-Migrate for database migrations
from iSaksham.app.routes.learning import blp as HomeBlueprint  # Importing blueprint for home routes
from iSaksham.app.routes.admin import blp as AuthBlueprint  # Importing blueprint for authentication routes
from flask_login import LoginManager, current_user  # Importing LoginManager and current_user for user authentication
from iSaksham.app.models.user import User  # Importing User model
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from iSaksham.app.routes.devloper import blp as DevBlueprint  # Importing blueprint for developer routes

# File path to store visit count
current_directory = os.getcwd()
VISIT_COUNT_FILE = current_directory + '/iSaksham/app/static/visit_count.txt'

# Function to read visit count from file
def read_visit_count():
    try:
        with open(VISIT_COUNT_FILE, 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

# Function to write visit count to file
def write_visit_count(count):
    with open(VISIT_COUNT_FILE, 'w') as f:
        f.write(f"{count:07d}")

# Function to convert number to a string with seven digits
def convert_to_seven_digits(number):
    return f"{number:07d}"

# Creating the Flask application
def create_app():
    app = Flask(__name__)  # Initializing Flask app
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/error.log', maxBytes=10240, backupCount=10)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] in %(module)s: %(message)s')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    
    app.config.update({
    "SESSION_COOKIE_SECURE": True,          # Only over HTTPS
    "SESSION_COOKIE_HTTPONLY": True,        # Not accessible via JS
    "SESSION_COOKIE_SAMESITE": "Lax"        # Or "Strict" for tighter control
})

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Your email address
    app.config['MAIL_PASSWORD'] = 'your_password'  # Your email password
    app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'  # Default sender
    # Configuring Flask app
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with your actual secret key
    # app.config['API_TITLE'] = 'pwa'
    # app.config['API_VERSION'] = 'v1'
    # app.config["OPENAPI_VERSION"] = "3.0.3"
    # app.config["OPENAPI_URL_PREFIX"] = "/"
    # app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    # app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://db_master:w24JyTn0SIEHfS@144.24.103.183:5432/isaksham_db'  # Replace with your actual database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    mail = Mail(app)
    db.init_app(app)  # Initializing the database with the Flask app
    # migrations_directory = current_directory + '/iSaksham/migrations'
    migrate = Migrate(app, db)  # Initializing Flask-Migrate with the Flask app
    app.register_blueprint(HomeBlueprint)  # Registering home blueprint with the Flask app
    app.register_blueprint(AuthBlueprint)  # Registering authentication blueprint with the Flask app
    app.register_blueprint(DevBlueprint)  # Registering chapters blueprint with the Flask app
    csrf = CSRFProtect(app)
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        return response

    login_manager = LoginManager()  # Initializing LoginManager
    login_manager.login_view = 'admin.login'  # Setting the login view
    login_manager.init_app(app)  # Initializing LoginManager with the Flask app
    
    # Function to load user for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @login_manager.unauthorized_handler
    def unauthorized():
        print("Unauthorized access to:", request.path)  # Debugging
        return redirect(url_for('admin.login', next=request.full_path))

    # Function to increment visit count before each request
    @app.before_request
    def increment_visit_count():
        
        if 'static' not in request.path:
            g.visit_count = read_visit_count()
            g.visit_count += 1
            write_visit_count(g.visit_count)
        

    # Context processor to inject data into templates
    @app.context_processor
    def inject_title():
        visit_count = convert_to_seven_digits(g.visit_count)
        if current_user.is_authenticated:
            name = current_user.name
        else:
            name = ""

        #average_rating = Feedback.get_average()
        average_rating = 0
        if not average_rating:
            average_rating = 0

        return {'visit_count': visit_count, 'name': name, 'average_rating': average_rating}
    
    @app.errorhandler(404)
    def page_not_found(error):
        app.logger.warning(f"404 Not Found: {request.url}")
        return render_template('developer/error.html', 
                            error_code=404, 
                            error_message="Page Not Found", 
                            description="The page you are looking for does not exist."), 404

    # Error handler for 500 Internal Server errors
    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error(f"500 Error: {request.url} - {error}")
        return render_template('developer/error.html', 
                            error_code=500, 
                            error_message="Internal Server Error", 
                            description="Something went wrong on our end. Please try again later."), 500

    # General error handler for other errors
    @app.errorhandler(Exception)
    def handle_exception(error):
        # Pass through HTTP errors
        if isinstance(error, HTTPException):
            return error
        # Print the traceback to the terminal
        traceback.print_exc()
        app.logger.error("Unhandled Exception", exc_info=error)
        app.logger.error(f"URL: {request.url}")
        app.logger.error(f"Payload: {session.get('payload', 'N/A')}")
        # Non-HTTP exceptions
        return render_template('developer/error.html', 
                            error_code=500, 
                            error_message="Unexpected Error", 
                            message = "Please report the bug in the feedback page with screenshot.",
                            description="An unexpected error occurred:"+str(error)), 500

    return app  # Returning the Flask app instance
