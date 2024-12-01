from flask import redirect, render_template, request,session,url_for
from eSaksham.app import create_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests

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

def get_auth_check():
    scheme = 'https://' if request.is_secure else 'http://'
    base_url=scheme+request.host
    req_url = base_url+ '/get_auth_json'
    headers = {'Content-Type': 'application/json'}
    reqUrl = "http://127.0.0.1:8080/get_auth_json"

    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }

    payload = ""

    response = requests.request("GET", reqUrl, data=payload,  headers=headersList)

    print(response.text)

@app.route('/')
# @jwt_required()  # Correct usage without parentheses
def serve_scorm_content():  # Get the user identity from the JWT token
    # print(get_auth_check())
    return redirect('/iauth/login')
    # if 'user_id' not in session:
    #     return redirect('/iauth/login')  # Redirect if the user is not authenticated
    
    # Logic to serve SCORM content (e.g., a SCORM package or HTML content)
    return render_template('story.html')  # Render your SCORM content

# Define other routes and logic for your Flask application
@app.route('/analytics-frame.html')
def render():
    return render_template('analytics-frame.html')

