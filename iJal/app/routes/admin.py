from flask import Blueprint, flash, get_flashed_messages, json, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from iJal.app.models.states import State
from iJal.app.models.users import User
from flask_login import current_user, login_required
from iJal.app.classes.block_data import BlockData
from iJal.app.routes.desktop import get_message
from iJal.app.classes.helper import HelperClass


blp = Blueprint("admin","admin")

@blp.route('/progress')
@login_required
def progress():
    if current_user.isAdmin:
        progress = State.get_all_states_status()

        return render_template('admin/progress.html',
                            progress=progress,
                            menu = HelperClass.get_admin_menu(),
                            progress_data = json.dumps(progress))
    else: 
        flash('You must be admin to view this page!')
        return redirect(url_for('auth.login'))

@blp.route('/home', methods=['POST','GET'])
@login_required
def home():
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
        return render_template('admin/approve.html',
                            users=users,
                            menu = HelperClass.get_admin_menu(),
                            user_data=json.dumps(users))
    else: 
        flash('You must be admin to view this page!')
        return redirect(url_for('auth.login'))
    
@blp.route('/status',methods=['POST','GET'])
def status():
    if request.method == 'POST':
        payload = request.json
        session['redirect_payload'] = payload
        return jsonify({'redirect_url': url_for('.status')})
    
    payload = session.get('redirect_payload')
    progress_status = BlockData.get_progress_status(block_id=payload['block_id'], 
                                            district_id=payload['district_id'], 
                                            state_id=payload['state_id'])
    return render_template('admin/status.html',
                           progress = progress_status,
                           flash_message = get_message(),
                           breadcrumbs=HelperClass.get_breadcrumbs(payload),
                           menu= HelperClass.get_admin_menu())
    
@blp.route('/dashboard',methods=['POST','GET'])
def dashboard():
    chart_data = HelperClass.get_dashboard_menu()
    card_data = HelperClass.get_card_data(chart_data)
            
    return render_template('admin/dashboard.html',
                           card_data = card_data,
                           chart_data = json.dumps(chart_data),
                           flash_message = get_message(),
                           menu= HelperClass.get_admin_menu())