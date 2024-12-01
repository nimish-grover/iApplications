from flask import jsonify,request,redirect,url_for,flash,render_template,session,make_response
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required,set_access_cookies,unset_access_cookies
from flask_smorest import Blueprint, abort
from iAuth.app.models.user import UserModel as User
from passlib.hash import pbkdf2_sha256
from flask_login import current_user, login_required, login_user, logout_user
from iAuth.app.routes.email_helper import *
from iAuth.app.models.inrole import inRoleModel
import uuid
import requests

blp = Blueprint("admin", "admin", description="User Authentication")

BASE_URL = 'https://training.wasca.in'
@blp.route('/profile')
def profile():
    return('profile')


@blp.route('/get_auth_json')
def get_auth_json():
    session_id = session.get('session_id', None)  # Will return None if 'session_id' is not in the session
    user_id = session.get('user_id', None)   
    if user_id and session_id:
        return jsonify({'message':'logged in','user_id':user_id,'session_id':session_id})
    else:
        return jsonify({'message':'Not Authenticated'})
    



# Route for login
@blp.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()       
        if user:
            db_email = user.email
            db_pass = user.password
            hash_check = pbkdf2_sha256.verify(password, db_pass)        
            if db_email == email and hash_check:
                login_user(user)
                session['user_id'] = user.id
                session_id = (uuid.uuid4())
                session['session_id'] = session_id
                return redirect('/')
                
                # return {"message":"Error generating JWT Token"}
            else:
                flash('Incorrect Credentials.')
                return redirect(url_for('admin.login'))
        else:
            flash('No Records Found !! Please validate your Credentials.')
            return redirect(url_for('admin.login'))
        
    return render_template('login.html')

# Route for user registration
@blp.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('username')
        password = pbkdf2_sha256.hash(request.form.get('password'))
        if email and name and password:

            user = User.get_user_by_email(email)
            if user:
                flash('Email address already exists')
                return redirect(url_for('admin.register'))

            user = User(name, email, password)
            session['user_email'] = email
            session['user_password'] = password
            session['user_name'] = name
            
            otp_details = send_email(email)
            
            if otp_details:
                session['otp_details'] = otp_details
                otp_message = f"Email has been sent to {email} Successfully. Please check your inbox (and spam folder) for the OTP."
                flash(otp_message)
                return redirect(url_for('admin.verify_otp'))

            else:
                flash("Email cannot be sent. Please try again later.")
                return redirect(url_for('admin.register'))
            
        
        else:
            return redirect(url_for('admin.register'))

    return render_template('register.html')


# Route for OTP verification
@login_required
@blp.route('/verify_otp', methods=["POST", "GET"])
def verify_otp():
    if request.method == "POST":
        name = session.get('user_name')
        password = session.get('user_password')
        email = session.get('user_email')
        otp_details = session.get('otp_details')
        otp_entered = request.form.get('otp')
        otp_generated = otp_details['otp']
        
        if int(otp_generated) == int(otp_entered):
            user = User(name, email, password)
            user.save_to_db()
            user_db = User.find_by_username(name)
            user_id = user_db['id']
            role_id = 1
            inrole = inRoleModel(user_id,role_id)
            inrole.save_to_db()
            
            flash("OTP Verified Successfully. Please login to continue")
            return redirect(url_for('admin.login'))
        else:
            flash("OTP cannot be verified. Please enter valid OTP")
            return redirect(url_for('admin.verify_otp'))
    return render_template('verify_otp.html')

# Route to resend OTP
@login_required
@blp.route('/resend_otp')
def resend_otp():
    email = session.get('user_email')
    otp_details = send_email(email)
            
    if otp_details:
        session['otp_details'] = otp_details
        otp_message = f"Email has been sent to {email}. Please check your inbox (and spam folder) for the OTP."
        flash(otp_message)
        return redirect(url_for('admin.verify_otp'))

    else:
        flash("Email cannot be sent. Please try again later.")
        return redirect(url_for('admin.verify_otp'))

# Route for logout
@blp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('session_id', None)  # 'None' ensures no error if key is absent
    session.pop('user_id', None)
    session['logged_out'] = True
    # Redirect to login page or any other URL
    # Clear the JWT cookie
    return redirect(url_for('admin.login'))

# Route for changing password
@blp.route('/change_password/<id>', methods=['GET', 'POST'])
@login_required
def change_password(id):

    if request.method == "POST":
            
        current_pwd = request.form.get('old_pass')
        new_pass = pbkdf2_sha256.hash(request.form.get('new_pass'))

        user = User.query.filter_by(id=id).first()       
        if user:
        
            db_pass = user.password
            hash_check = pbkdf2_sha256.verify(current_pwd, db_pass)        
            if hash_check:
                data = {"password": new_pass}
                User.update_db(data, id)
                logout_user()
                session['logged_out'] = True   
                flash('Password Changed Successfully. Please login with new password to continue')
                return redirect(url_for('admin.login'))
            
            else:
                flash('Please Check Your Old Password and Try Again !! ')
                return redirect(url_for('admin.change_password', id=id))
    
    if request.method == "GET":
        return render_template('change_password.html')

# Route for verifying email
@login_required
@blp.route('/verify_email', methods=["POST", "GET"])
def verify_email():
    if request.method == "POST":
        new_pass = session.get('new_pass')
        otp_details = session.get('otp_details')
        otp_entered = request.form.get('otp')
        otp_generated = otp_details['otp']
        
        if int(otp_generated) == int(otp_entered):
            data = {"password": new_pass}
            User.update_db(data, current_user.id)   
            logout_user()
            session['logged_out'] = True
            flash("OTP Verified Successfully. Please login with new password continue")
            return redirect(url_for('admin.login'))
        else:
            flash("OTP cannot be verified. Please enter valid OTP")
            return redirect(url_for('admin.verify_email'))
    return render_template('verify_email.html')

# Route for resetting password
@login_required
@blp.route('/reset_password/<id>', methods=['POST', 'GET'])
def reset_password(id):
    if request.method == "GET":
        return render_template('reset_password.html')
    else:
        user = User.query.filter_by(id=id).first()
        new_pass = pbkdf2_sha256.hash(request.form.get('new_pass'))
        session['new_pass'] = new_pass
        email = user.email
        otp_details = send_email(email)
            
        if otp_details:
            session['otp_details'] = otp_details
            otp_message = f"OTP has been sent to registered email Successfully. Please check your inbox (and spam folder) for the OTP."
            flash(otp_message)
            return redirect(url_for('admin.verify_email'))

        else:
            flash("Email cannot be sent. Please try again later.")
            return redirect(url_for('admin.register'))

# Route for the page that doesn't require login
@blp.route('/no_login')
def no_login():
    return render_template('no_login.html')  # Rendering no_login.html template

@blp.route('/admin')
def admin():
    return render_template('admin.html')
