from flask import render_template,request
from iCore.app import create_app

app = create_app()
app.debug = True

@app.route('/')
def hello_world():
    return render_template('index.html')

# @app.before_request
# def log_request():
#     print(f"Request to {request.path}")