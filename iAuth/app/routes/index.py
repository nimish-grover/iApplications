from flask_smorest import Blueprint
from flask import render_template

blp = Blueprint('dashboard','dashboard')

@blp.route('/')
def hello_world():
    return render_template('index.html')

@blp.route('/get_page')
def new():
    return render_template('admin_base.html')