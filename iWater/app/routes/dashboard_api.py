from flask_smorest import Blueprint
from iWater.app.models.water_bodies import Water_bodies
from flask import request


blp = Blueprint("api", "api", description="API Routes")



@blp.route('/get_bubble_chart_values',methods=['POST','GET'])
def bubble_chart():
    json_data={}

    if request.is_json:
        json_data = request.json
    
    db = Water_bodies.bubble_chart_values(json_data)
    array=[]
    for row in db:
        array.append(list(row))
        # json_object[row[4]] = list(row)
    
    return array


@blp.route('/get_doughnut_chart_values',methods=['POST','GET'])
def doughnut_chart():
    json_data={}
    
    if request.is_json:
        json_data = request.json
    
    db = Water_bodies.doghnut_chart_values(json_data)
    array=[]
    for row in db:
        array.append(list(row))
        # json_object[row[4]] = list(row)
    
    return array

@blp.route('/get_top_five',methods=['POST','GET'])
def doughnut_chart():
    json_data={}
    if request.is_json:
        json_data = request.json
    
    db = Water_bodies.get_top_five(json_data)
    array=[]
    for row in db:
        array.append(list(row))
        # json_object[row[4]] = list(row)
    
    return array


@blp.route('/get_count_sum',methods=['POST','GET'])
def doughnut_chart():
    json_data={}
    if request.is_json:
        json_data = request.json
    
    db = Water_bodies.get_count_sum(json_data)
    array=[]
    for row in db:
        array.append(list(row))
        # json_object[row[4]] = list(row)
    
    return array

