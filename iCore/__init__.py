from flask import render_template
from iCore.app import create_app

app = create_app()
app.debug = True

@app.route('/')
def hello_world():
    return render_template('index.html')