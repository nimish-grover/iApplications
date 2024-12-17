from flask import Blueprint, flash, get_flashed_messages, json, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from iJal.app.models.states import State
from iJal.app.models.territory import TerritoryJoin
from iJal.app.models.users import User

blp = Blueprint("auth","auth")

@blp.route('/register', methods=['POST','GET'])
def register():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        state_id = request.form.get('dd_states')
        user = User.find_by_username(username.lower())
        if user:
            flash('username already exists!')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('auth.register'))

        user = User(username.lower(), password,state_id, False, False)
        user.set_password(password)
        user.save_to_db()

        flash('Registered successfully!')
        return redirect(url_for('auth.login'))
    states = TerritoryJoin.get_aspirational_states()
    message = get_message()
    return render_template("auth/register_user.html", 
                           flash_message=message, states = states)

@blp.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username.lower()).first()
        if user and User.check_password(user, password) and user.isActive:
            login_user(user)
            return redirect(url_for('mobile.index'))
        elif user is None:
            flash('User does not exist!')
        elif not User.check_password(user, password):
            flash('Password is incorrect')
        elif not user.isActive:
            flash('User is not authorized. Please contact State Coordinator')
    message = get_message()
    return render_template('auth/login.html', flash_message = message)

@blp.route('/logout')
def logout():
    logout_user()
    session.clear()
    session['logged_out']=True
    return redirect(url_for('.login'))

@blp.route('/change_password')
@login_required
def change_password():
    return render_template("auth/change_password.html")

@blp.route('/forgot_password')
@login_required
def forgot_password():
    return render_template("auth/forgot_password.html")

@blp.route('/reset_password')
@login_required
def reset_password():
    return render_template("auth/reset_password.html")

@blp.route('/approve', methods=['POST','GET'])
@login_required
def approve():
    if request.method =='POST':
        json_data = request.json
        for item in json_data:
            if item['id']:
                user_object = User.get_by_id(item['id'])
                user_object.isActive = bool(item['isActive'])
                user_object.update_db()
        flash("The user(s) is/are approved!!")
        return jsonify({'redirect_url': url_for('mobile.index')})
    if current_user.isAdmin:
        users = User.get_all()
        # states = State.get_all()
        return render_template('auth/approve.html',
                           users=users,
                           user_data=json.dumps(users))
    else: 
        flash('You must be admin to view this page!')
        return redirect(url_for('auth.login'))

def get_message():
    messages = get_flashed_messages()
    if len(messages) > 0:
        message = messages[0]
    else:
        message = ''

    return message
