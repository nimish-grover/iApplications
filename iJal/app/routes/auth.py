from flask import Blueprint, flash, get_flashed_messages, redirect, render_template, request, session, url_for,json,jsonify
from flask_login import login_user, logout_user
from iJal.app.models.territory import TerritoryJoin
from iJal.app.models.users import User
from iJal.app.models.states import State

blp = Blueprint("auth","auth")

@blp.route('/register', methods=['POST','GET'])
def register():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
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
    states = TerritoryJoin.get_aspirational_states()
    message = get_message()
    return render_template("auth/register_user.html", flash_message=message, states = states)

@blp.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
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

@blp.route('/approve',methods=['POST','GET'])
def approve():
    if request.method =='POST':
        json_data = request.json
        for item in json_data:
            if item['table_id']:
                user_object = User.get_by_id(item['table_id'])
                user_object.isActive = True if item['isactive'] == 'Approve' else False
                user_object.state_id = State.get_id_by_name(item['state'])
                user_object.update_db()
        return jsonify({'redirect_url': url_for('.approve')})
    users = User.get_all()
    states = State.get_all()
    return render_template('auth/approve.html',users=users,user_data=json.dumps(users),states=states)

@blp.route('/logout')
def logout():
    logout_user()
    session.clear()
    session['logged_out']=True
    return redirect(url_for('.login'))

@blp.route('/change_password')
def change_password():
    return render_template("auth/change_password.html")

@blp.route('/forgot_password')
def forgot_password():
    return render_template("auth/forgot_password.html")

@blp.route('/reset_password')
def reset_password():
    return render_template("auth/reset_password.html")


def get_message():
    messages = get_flashed_messages()
    if len(messages) > 0:
        message = messages[0]
    else:
        message = ''

    return message
