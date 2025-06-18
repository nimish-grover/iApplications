import csv
from datetime import datetime
from functools import wraps
from io import StringIO
import os
import random
import uuid
from flask import abort, flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user,login_manager
from flask_smorest import Blueprint
from passlib.hash import pbkdf2_sha256
import requests
from iSaksham.app.db import db
from iSaksham.app.models.feedback import Feedback
from iSaksham.app.models.user import User
from iSaksham.app.models.activity_log import ActivityLog
from iSaksham.app.routes.email_helper import send_email, send_new_user_email, send_reset_email
from flask_wtf.csrf import CSRFProtect

blp = Blueprint("admin", "admin","Authorisation related routes")

CAPTCHA_SECRET_KEY = os.getenv('CAPTCHA_SECRET_KEY',' ')

# Route for login
@blp.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        recaptcha_response = request.form.get('g-recaptcha-response')
        
        # If no response was provided, reject the submission
        if not recaptcha_response:
            flash('Please check the reCAPTCHA box.')
            return render_template('login.html')
        
        
        # Verify the reCAPTCHA response
        verification_response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': CAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
        )
        
        verification_result = verification_response.json()
        if not verification_result.get('success'):
            flash('reCAPTCHA verification failed. Please try again.')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()       
        if user:
            db_email = user.email
            db_pass = user.password
            hash_check = pbkdf2_sha256.verify(password, db_pass)        
            if db_email == email and hash_check:
                login_user(user, remember=remember)
                next_page = '/isaksham'+ request.form.get('next')
                return redirect(next_page) if next_page else redirect(url_for('learning.home'))
                
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
        recaptcha_response = request.form.get('g-recaptcha-response')
        
        
        # If no response was provided, reject the submission
        if not recaptcha_response:
            flash('Please check the reCAPTCHA box.')
            return render_template('register.html')
        
        
        # Verify the reCAPTCHA response
        verification_response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': CAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
        )
        
        verification_result = verification_response.json()
        if not verification_result.get('success'):
            flash('reCAPTCHA verification failed. Please try again.')
            return render_template('register.html')
        if email and name and password:

            user = User.get_user_by_email(email)
            if user:
                flash('Email address already exists')
                return redirect(url_for('admin.register'))

            
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
@blp.route('/verify_otp', methods=["POST", "GET"])
def verify_otp():
    if request.method == "POST":
        name = session.get('user_name')
        password = session.get('user_password')
        email = session.get('user_email')
        otp_details = session.get('otp_details')
        otp_entered = request.form.get('otp')
        otp_generated = otp_details['otp']
        is_active = True
        is_admin = False
        if int(otp_generated) == int(otp_entered):
            user = User(name, email, password,is_active, is_admin)
            user.save_to_db()

            flash("OTP Verified Successfully. Please login to continue")
            return redirect(url_for('admin.login'))
        else:
            flash("OTP cannot be verified. Please enter valid OTP")
            return redirect(url_for('admin.verify_otp'))
    return render_template('verify_otp.html')

# Route to resend OTP
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
    session['logged_out'] = True
    return redirect(url_for('learning.home'))

# Route for changing password
@blp.route('/change_password/<string:uuid>', methods=['GET', 'POST'])
@login_required
def change_password(uuid):

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
@blp.route('/verify_email', methods=["POST", "GET"])
@login_required
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
@blp.route('/reset_password/<string:uuid>', methods=['POST', 'GET'])
@login_required
def reset_password(uuid):
    if request.method == "GET":
        return render_template('reset_password.html')
    else:
        user = User.query.filter_by(id=id).first()
        new_pass = pbkdf2_sha256.hash(request.form.get('new_pass'))
        session['new_pass'] = new_pass
        session['user_name'] = user.name
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


# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

@blp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get all users - we'll do sorting and filtering client-side
    users = User.query.all()
    
    return render_template(
        'admin_dashboard.html',
        users=users,
        page=1,
        total_pages=1
    )

@blp.route('/toggle-user-status/<string:user_uuid>', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_uuid):
    try:
        data = request.get_json()
        is_active = data.get('is_active', False)
        
        user = User.query.filter_by(uuid=user_uuid).first_or_404()
        user.is_active = is_active
        
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blp.route('/reset-password/<string:user_uuid>', methods=['POST'])
@login_required
@admin_required
def reset_password(user_uuid):
    try:
        data = request.get_json()
        default_password = data.get('default_password')
        
        user = User.query.filter_by(uuid=user_uuid).first_or_404()
        
        # Update password with the default password
        user.password = pbkdf2_sha256.hash(default_password)
        db.session.commit()
        send_reset_email(user.email, user.name)
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blp.route('/log-activity', methods=['POST'])
@login_required
@admin_required
def log_activity():
    try:
        data = request.get_json()
        user_uuid = data.get('user_uuid')
        action = data.get('action')
        timestamp = data.get('timestamp')
        
        # Convert timestamp string to datetime
        if timestamp:
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        else:
            timestamp = datetime.utcnow()
        
        # Determine user_id from uuid
        if user_uuid == 'admin':
            # Log action as the current admin
            user_id = current_user.id
        else:
            user = User.query.filter_by(uuid=user_uuid).first()
            if not user:
                return jsonify({'success': False, 'message': 'User not found'})
            user_id = user.id
        
        # Create activity log
        activity_log = ActivityLog(
            user_id=user_id,
            action=action,
            timestamp=timestamp
        )
        
        db.session.add(activity_log)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@blp.route('/delete-user/<string:user_uuid>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_uuid):
    user = User.query.filter_by(uuid=user_uuid).first_or_404()
    
    try:
        # Delete user
        db.session.delete(user)
        db.session.commit()
        
        # flash(f'Successfully deleted user: {user.name}')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}')
    
    return redirect(url_for('admin.dashboard'))

@blp.route('/export-users')
@login_required
@admin_required
def export_users():
    try:
        # Create a CSV string
        csv_data = StringIO()
        csv_writer = csv.writer(csv_data)
        
        # Write header
        csv_writer.writerow([
            'UUID', 'Name', 'Email', 'Status', 'Admin', 'Registration Date'
        ])
        
        # Write user data
        users = User.query.all()
        for user in users:
            csv_writer.writerow([
                user.uuid,
                user.name,
                user.email,
                'Active' if user.is_active else 'Inactive',
                'Yes' if user.is_admin else 'No',
                user.registered_on.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        # Create response
        from flask import Response
        response = Response(
            csv_data.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename=users_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            }
        )
        return response
    except Exception as e:
        flash(f'Error exporting users: {str(e)}')
        return redirect(url_for('admin.dashboard'))

@blp.route('/add-user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = email[:4]+'_123@'
        is_active = 'is_active' in request.form
        is_admin = 'is_admin' in request.form
        
        # Validate input
        if not name or not email or not password:
            flash('Name, email and password are required')
            return redirect(url_for('admin.add_user'))
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('A user with this email already exists')
            return redirect(url_for('admin.add_user'))
        
        try:
            
            # Create new user
            new_user = User(
                name=name,
                email=email,
                password=pbkdf2_sha256.hash(password),
                is_active=is_active,
                is_admin=is_admin
            )
            
            db.session.add(new_user)
            db.session.commit()
            send_new_user_email(email, name)
            # Log activity
            activity_log = ActivityLog(
                user_id=current_user.id,
                action=f"Created new user: {name} ({email})"
            )
            db.session.add(activity_log)
            db.session.commit()
            
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating user: {str(e)}')
            return redirect(url_for('admin.add_user'))
    
    # GET request - show the form
    return render_template('add_user.html')

@blp.route('/view_feedback')
@login_required
@admin_required
def view_feedback():
    # Get all feedback entries
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    
    return render_template('view_feedback.html', feedbacks=feedbacks)

@blp.route('/export-feedback')
@login_required
@admin_required
def export_feedback():
    try:
        # Create a CSV string
        csv_data = StringIO()
        csv_writer = csv.writer(csv_data)
        
        # Write header
        csv_writer.writerow([
            'ID', 'Name', 'Email', 'Subject', 'Category', 'Message', 'Rating', 
            'Has Image', 'Date Created'
        ])
        
        # Write feedback data
        feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
        for feedback in feedbacks:
            csv_writer.writerow([
                feedback.id,
                feedback.name,
                feedback.email,
                feedback.subject,
                feedback.message_category,
                feedback.message,
                feedback.rating,
                'Yes' if feedback.image_filename else 'No',
                feedback.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        # Log activity
        log_activity(current_user.id, f"Exported feedback data ({len(feedbacks)} entries)")
        
        # Create response
        from flask import Response
        response = Response(
            csv_data.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename=feedback_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            }
        )
        return response
    except Exception as e:
        flash(f'Error exporting feedback: {str(e)}')
        return redirect(url_for('admin.view_feedback'))

# Helper function for Jinja templates to convert newlines to <br> tags
@blp.app_template_filter('nl2br')
def nl2br(value):
    if not value:
        return ''
    return value.replace('\n', '<br>')