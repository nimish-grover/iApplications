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
        status_dummy = [{'category':'Human','id':'population'},
                        {'category':'Livestocks','id':'livestock'},
                        {'category':'Crops','id':'crop'},
                        {'category':'Industry','id':'industry'},
                        {'category':'Surface','id':'surface'},
                        {'category':'Groundwater','id':'ground'},
                        {'category':'LULC','id':'lulc'},
                        {'category':'Rainfall','id':'rainfall'},
                        {'category':'Water Transfer','id':'water_transfer'}]
        return render_template('admin/progress.html',
                            progress=progress,
                            status = status_dummy,
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
    

    
@blp.route('/dashboard',methods=['POST','GET'])
def dashboard():
    chart_data = HelperClass.get_dashboard_menu()
    card_data = HelperClass.get_card_data(chart_data)
            
    return render_template('admin/dashboard.html',
                           card_data = card_data,
                           chart_data = json.dumps(chart_data),
                           flash_message = get_message(),
                           menu= HelperClass.get_admin_menu())