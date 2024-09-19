from flask import redirect, render_template, request
from eSaksham.app import create_app
from flask_jwt_extended import jwt_required, get_jwt_identity

app = create_app()
app.debug = True

@app.errorhandler(404)
def not_found_error(error):
    # Check if the request path does not start with '/scorm'
    if not request.path.startswith('/scorm') and 'favicon' not in request.path:
        # Modify the path by adding '/scorm' at the beginning
        modified_path = '/esaksham/scorm' + request.path
        # Redirect to the modified path
        return redirect(modified_path)
    elif request.path.startswith('/scorm'):
        modified_path = '/esaksham' + request.path
        return redirect(modified_path)
    elif not request.path.startswith('/esaksham/scorm'):
        modified_path = '/esaksham/scorm' + request.path
        return redirect(modified_path)
    elif request.path.startswith('/story_content'):
        modified_path = '/esaksham/scorm' + request.path
        return redirect(modified_path)
    # If the request path already starts with '/scorm', return the original 404 error
    return error

@app.route('/')
@jwt_required()  # Correct usage without parentheses
def serve_scorm_content():
    current_user = get_jwt_identity()  # Get the user identity from the JWT token
    if not current_user:
        return redirect('/iauth/login')  # Redirect if the user is not authenticated
    
    # Logic to serve SCORM content (e.g., a SCORM package or HTML content)
    return render_template('story.html')  # Render your SCORM content

# Define other routes and logic for your Flask application
@app.route('/analytics-frame.html')
def render():
    return render_template('analytics-frame.html')

