from flask import Blueprint, abort, flash, get_flashed_messages, redirect, render_template, request, session, url_for
from flask_login import login_user, logout_user

from iJalagam.app.models.users import User


blp = Blueprint('auth', 'auth')

@blp.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and User.check_password(user, password):
            login_user(user)
            # next_page = request.args.get('next')

            # if not next_page and request.referrer:
            #     if '?next' in request.referrer:
            #         referrer_url = urlparse(request.referrer)
            #         query_params = parse_qs(referrer_url.query)
            #         next_page = query_params.get('next', [None])[0]  # Get 'next' param or None
            
            # if next_page and is_safe_url(next_page):
            #     return redirect(next_page)
            return redirect(url_for('routes.select_block'))
    
    return render_template('auth/login.html')

@blp.route('/register', methods=['POST','GET'])
def register():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user = User.find_by_username(username)
        if user:
            flash('username already exists!')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('auth.register'))

        user = User(username, password, False, False)
        user.set_password(password)
        user.save_to_db()

        flash('Registered successfully!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register_user.html')

@blp.route('/')
def splash():
    return render_template('splash_screen.html')

@blp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@blp.route('/change_password')
def change_password():
    return render_template('auth/change_password.html')

from urllib.parse import parse_qs, urlparse, urljoin

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc



