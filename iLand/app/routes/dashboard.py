from flask import flash, redirect, render_template, request, session, url_for
from flask_smorest import Blueprint
import plotly.graph_objs as go
import plotly.io as pio
from iLand.app.models.wl_area import WL_Area
from iLand.app.models.state import State
from iLand.app.models.tga import Tga
from iLand.app.models.districts import District
from iLand.app.models.state import State
import random


blp = Blueprint("dashboard", "state_wise","state wise waste land area ")

@blp.route('/')
def dashboard():
    # horizontal bars
    db_state_wise = WL_Area.get_area_state_wise(2)
    labels_statewise = []
    values_statewise = []
    for item in db_state_wise:
        labels_statewise.append(item[0].title())
        values_statewise.append(item[1])
    
    
    #category doughnut
    labels_categorywise = []
    values_categorywise = []
    category_area = WL_Area.get_area_category_wise_nation(2)
    for item in category_area:
        labels_categorywise.append(item[0].title())
        values_categorywise.append(item[1])
    
    #total_wl
    total_wl_area = WL_Area.get_total_area(2) 
    
    #total_tga
    total_tga = Tga.get_total_tga()
    
    #random state gauge
    random_state_code = random.randint(1,36)
    db_by_state = WL_Area.get_area_by_state_code(random_state_code,2)
    if not db_by_state: 
        db_by_state = WL_Area.get_area_by_state_code(8,2)
    state_gauge_values = [db_by_state[0][2],db_by_state[0][3]]
    state_gauge_name = db_by_state[0][1]
    state_gauge_code = db_by_state[0][0]
    
    #random district vertical bar 
    random_district_code = random.randint(1,760)
    labels_district_category = []
    values_district_category = []
    
    district_data = WL_Area.get_area_category_wise_district(random_district_code,2)
    if district_data:
        district_db = District.get_district_by_code(random_district_code)
        district_bar_name = district_db['name']
        district_bar_code = district_db['code']
        
        for item in district_data:
            if item[1]:
                labels_district_category.append(item[0])
                values_district_category.append(item[1])
    else:
        random_district_code = 145
        district_data = WL_Area.get_district_area_category_wise(random_district_code,2)
        district_db = District.get_district_by_code(random_district_code)
        district_bar_name = district_db['name']
        district_bar_code = district_db['code']
        
        for item in district_data:
            if item[1]:
                labels_district_category.append(item[0])
                values_district_category.append(item[1])
        
    
    return render_template('dashboard.html',
                        labels_statewise = labels_statewise,
                        values_statewise = values_statewise,
                        values_categorywise = values_categorywise,
                        labels_categorywise = labels_categorywise,
                        total_wl_area = total_wl_area,
                        total_tga = total_tga,
                        state_gauge_name = state_gauge_name,
                        state_gauge_values = state_gauge_values,
                        labels_district_category = labels_district_category,
                        values_district_category = values_district_category,
                        district_bar_code = district_bar_code,
                        district_bar_name = district_bar_name
                        )


# all nation state wise wl area
@blp.route('/state_wise_area',methods = ["POST","GET"])
def state_wise_area():
    if request.method == "POST":
        state_code = request.form.get('state')
        return redirect(url_for('dashboard.district_wise_area',code = state_code))
    
    if request.method == "GET":
        states = State.get_all()
        return redirect(url_for('dashboard.district_wise_area',code= 0))

    
@blp.route('/district_wise_area/<int:code>')
def district_wise_area(code):
    if code == 0:
        title= 'State Wise Area'
        db = WL_Area.get_area_state_wise(2)
        labels = []
        values = []
        for item in db:
            labels.append(item[0].title())
            values.append(item[1])
            
        states = State.get_all()
        return render_template('state_wise.html',state_wise_label = labels,state_wise_value = values,states = states,title=title)

    labels = []
    values = []
    districts_area = WL_Area.get_area_district_wise(code,2)
    state_db = State.get_state_by_code(code)
    for item in districts_area:
        labels.append(item[0].title())
        values.append(item[1])
    
    title = state_db['name'] + ' Waste Land Area'
    states = State.get_all()
    return render_template('state_wise.html', state_wise_label = labels, state_wise_value = values,states=states,title = title)


@blp.route('/category_wise_area',methods = ["POST","GET"])
def category_wise_area():
    if request.method == "POST":

        state_code = int(request.form.get('state_code'))
        if state_code:
            district_code = request.form.get('district_code')
            if district_code:
                district_code = int(district_code)
        if state_code == 0 :
            return redirect(url_for('dashboard.doughnut_area_nation'))
        
        elif district_code:
            return redirect(url_for('dashboard.doughnut_area_district',code=district_code))
        
        elif state_code:
            return redirect(url_for('dashboard.doughnut_area_state',code=state_code))
        

    
    if request.method == "GET":
        return redirect(url_for("dashboard.doughnut_area_nation"))


@blp.route('/doughnut_area_nation')
def doughnut_area_nation():
    labels = []
    values = []
    title= 'Category Wise Area'
    category_area = WL_Area.get_area_category_wise_nation(2)
    for item in category_area:
        labels.append(item[0].title())
        values.append(item[1])
    states = State.get_all()
        
    return render_template('category_wise.html', category_wise_label = labels, category_wise_value = values,title = title,states = states)

@blp.route('/doughnut_area_state/<int:code>')
def doughnut_area_state(code):
    if code :
        labels = []
        values = []
        category_area = WL_Area.get_area_category_wise_state(code,2)
        for item in category_area:
            labels.append(item[0].title())
            values.append(item[1])
        states = State.get_all()  
        if code:
            state_db = State.get_state_by_code(code)
            title = state_db['name']
        return render_template('category_wise.html', category_wise_label = labels, category_wise_value = values,title = title,states = states)
    else:
        return redirect(url_for('dashboard.doughnut_area_nation'))

@blp.route('/doughnut_area_district/<int:code>')
def doughnut_area_district(code):
    labels = []
    values = []
    category_area = WL_Area.get_area_category_wise_district(code,2)
    for item in category_area:
        labels.append(item[0].title())
        values.append(item[1])
    states = State.get_all()
    district_db = District.get_district_by_code(code)
    title = district_db['name']
    if not(category_area):
        flash('Data for this district not available in the database.')
    return render_template('category_wise.html', category_wise_label = labels, category_wise_value = values,title = title,states = states)


@blp.route('/national_gauge')
def national_gauge():
    values =[]
    tga = Tga.get_total_tga()
    wl_area = WL_Area.get_total_area(2)
    
    values.append(wl_area)
    values.append(tga)
    return render_template('national_gauge.html', national_gauge_value = values)

@blp.route('/state_area')
def state_area():
    state_db = WL_Area.get_area_sorted_state_wise(2)
    state_data = {}
    for index,item in enumerate(state_db):
        data = []
        data = [item[0],item[1].title(),item[2],item[3]]
        state_data[index] = data
    return state_data

@blp.route('/state_gauge')
def state_gauge():    
    return render_template('state_gauge.html')

@blp.route('/district_area/<int:code>')
def district_area(code):
    district_db = WL_Area.get_area_sorted_district_wise(code,2)
    district_data = {}
    for index,item in enumerate(district_db):
        data = []
        data = [item[0],item[1].title(),item[2],item[3]]
        district_data[index] = data
    return district_data

@blp.route('/district_gauge/<int:code>')
def district_gauge(code):
    district_db = District.get_district_by_state_code(code)
    state_data = State.get_state_by_code(code)
    return render_template('district_gauge.html',state_code = code, district_db = district_db, db_len = len(district_db), state_data = state_data)

@blp.route('/district_category/<int:code>')
def district_category(code):
    labels = []
    values = []
    district_db = District.get_district_by_code(code)
    district_data = WL_Area.get_area_category_wise_district(code,2)
    for item in district_data:
        if item[1]:
            labels.append(item[0])
            values.append(item[1])
            
        
    return render_template('district_category.html', category_wise_label = labels, category_wise_value = values, district_db = district_db)


@blp.route('/get_districts/<int:code>')
def get_districts(code):
    db = District.get_district_by_state_code(code)
    return db