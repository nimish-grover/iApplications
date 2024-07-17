from flask_smorest import Blueprint
from iWater.app.models.crop_area import Crop_area
from iWater.app.models.crops_type import Crops_type                 
from iWater.app.models.crops import Crops
from flask import jsonify, render_template,request,session,Response
from iWater.app.routes.water_budget import WaterBudgetCalc
from iWater.app.models.livestocks import Livestock
from iWater.app.models.livestock_census import LivestockCensus
from iWater.app.models.village import Village
from iWater.app.models.water_bodies_mp import Water_bodies_mp
from iWater.app.models.wb_master import WB_master
from iWater.app.models.block import Block
from iWater.app.models.district import District
from iWater.app.models.state import State
from iWater.app.db import db
import csv

blp = Blueprint('village_water_budget','village_water_budget')

@blp.route('/get_crops_data')
def get_crop_area():
    
    states = WaterBudgetCalc.get_states()
        
    return render_template('crop_data.html',states = states,crops_table = False)


@blp.route('/display_requirement_table', methods=['POST','GET'])
def display_requirement_table():
    village_code = request.form.get('ddVillages')
    json_data = {"village_code": village_code}
    print(json_data)
    states = WaterBudgetCalc.get_states()
    area_db = Crop_area.get_crop_area(json_data)
    total_crop_type = Crop_area.get_total_crop_types(json_data)
    
    water_req = []
    for i in range(total_crop_type):
        water_req.append([])
        for item in area_db:
            if item[4] == i+1:
                present_water = item[2]*item[3]
                groundwater_supply = (present_water*80)/100
                additional_requirement = present_water - groundwater_supply
                
                row = tuple(item[:4]) + (round(present_water,2),round(groundwater_supply,2),round(additional_requirement,2))
                water_req[i].append(row)
                
    print(water_req)
    # return water_req
    return render_template('crop_data.html',states = states,water_required = water_req, crops_table = True,total_crop_type = total_crop_type)

@blp.route('/add_data')
def add_data():
    # crop_type = Crops_type.get_all()
    # rabi_crops = Crops.get_by_type_id(2)
    # states = WaterBudgetCalc.get_states()
    # livestocks = Livestock.get_all()
    breadcrumbs = session['breadcrumbs']
    return render_template('add_data.html',breadcrumbs = breadcrumbs)

@blp.route('/add_agriculture_data', methods=['POST'])
def add_agriculture_data():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    
    crop_name = data['crop_name']
    crop_area = data['crop_area']
    coefficient = data['coefficient']
    district_code = data['district']
    village_code = data['village']
    crop_type_id = data['crop_type']
    
    crop_data = Crops.check_existing(crop_name)
    if crop_data:
        crop_id = crop_data['id']
    else:
        crop_data = Crops(crop_type_id,crop_name,coefficient)
        crop_data.save_to_db()
        crop_db = Crops.check_existing(crop_name)
        crop_id = crop_db['id']
        
    try:
        
        crop_area = Crop_area(district_code,village_code,crop_id,crop_type_id,crop_area)
        crop_area.save_to_db()
        print(f"Inserting into database: {data}")
        # Return success response
        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    

    
@blp.route('/add_human_to_db',methods=['POST'])
def add_human_to_db():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    
    # print(json_data)
    return json_data

@blp.route('/add_agriculture_to_db',methods=['POST'])
def add_agriculture_to_db():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    else:
        payload = session.get('payload')
        village_id = payload['village_id']
        for item in json_data:
            crop_type = item['cropType']
            crop_type_db = Crops_type.get_by_type(crop_type)
            crop_type_id = crop_type_db['id']
            crop_name = item['cropName']
            crop_db = Crops.get_by_name(crop_name)
            crop_id = crop_db['id']
            area = item['area']
            village_db = Village.get_district_by_village(village_id)
            district_id = village_db['district_id']
            payload['crop_id'] = crop_id
            payload['district_id'] = district_id
            payload['crop_type_id'] = crop_type_id
            check_existing = Crop_area.get_existing_data(payload)
            if check_existing:
                data = {'id': check_existing['id'], 'district_code': district_id, 'village_code': village_id, 'crop_id': crop_id, 'crop_type_id':crop_type_id, 'crop_area': area}
                updated_data = Crop_area.update_db(data,check_existing['id'])
                return jsonify({'message':'Data Stored'}), 200 
            else:
                data = Crop_area(district_id,village_id,crop_id,crop_type_id,area)
                data.save_to_db()
                return jsonify({'message':'Data Stored'}), 200
    # print(json_data)
    return json_data

@blp.route('/add_livestock_to_db',methods=['POST'])
def add_livestock_to_db():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    # print(json_data)
    else:
        payload = session.get('payload')
        village_id = payload['village_id']
        for item in json_data:
            population_size = item['populationSize']
            livestock_name = item['livestockName']
            livestock_type = item['livestockType']
            livestock_db= Livestock.get_by_name(livestock_name.lower())
            livestock_id = livestock_db['id']
            existing_check = LivestockCensus.get_existing_data(payload,livestock_id)
            if existing_check:
                data = {'id':existing_check['id'],'livestock_number': population_size,'livestock_id': livestock_id,'village_id': village_id}
                update_data = LivestockCensus.update_db(data,existing_check['id'])
                return jsonify({'message':'Data Stored'}), 200
            else:
                data = LivestockCensus(population_size,livestock_id,village_id)
                data.save_to_db()
                return jsonify({'message':'Data Stored'}), 200


@blp.route('/get_crops/<crop_type>')
def get_crops(crop_type):
    crop_type_id = Crops_type.get_by_type(crop_type)
    crops = Crops.get_by_type_id(crop_type_id['id'])
    # print(crops)
    crop_data = []
    for crop in crops:
        crop_data.append({'id':crop.id,'name':crop.name})
    return crop_data

@blp.route('/get_livestocks/<livestock_type>')
def get_livestocks(livestock_type):
    livestocks = Livestock.get_by_type(livestock_type.lower())
    
    # print(crops)
    livestock_data = []
    for livestock in livestocks:
        livestock_data.append({'id':livestock.id,'name':str(livestock.name).capitalize()})
    return livestock_data
# @blp.route('/correct_db')
# def correct_db():
#     crop_data = Crop_area(33,22,2,2,1)
#     crop_data.save_to_db()
#     return True

@blp.route('/add_harvest_data')
def add_harvest_data():
    breadcrumbs = session['breadcrumbs']
    water_body_db = WB_master.get_all()
    water_bodies = []
    for water_body in water_body_db:
        water_bodies.append(water_body.name)
    print(water_bodies)
    return render_template('harvest_data.html',breadcrumbs = breadcrumbs,water_bodies = water_bodies)



@blp.route('/add_waterbody_to_db',methods=['POST'])
def add_waterbody_to_db():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    
    else:
        payload = session.get('payload')
        village_id = payload['village_id']
        for item in json_data:
            waterbody_area = item['area']
            waterbody_name = item['waterbodyName']
            waterbody_db= WB_master.get_wb_by_name(waterbody_name)
            waterbody_type_id = waterbody_db['id']
            existing_check = Water_bodies_mp.get_existing_data(payload,waterbody_type_id)
            if existing_check:
                data = {'id':existing_check['id'],'district_code': existing_check['district_code'],'village_code': existing_check['village_code'],
                        'wb_type_id': existing_check['wb_type_id'],'water_spread_area': waterbody_area,
                        'max_depth':existing_check['max_depth'], 'storage_capacity':existing_check['storage_capacity'],'longitude':['longitude'],'latitude':existing_check['latitude']}
                update_data = Water_bodies_mp.update_db(data,existing_check['id'])
                return jsonify({'message':'Data Stored'}), 200
            else:
                # data = LivestockCensus(waterbody_area,livestock_id,village_id)
                # data.save_to_db()
                return jsonify({'status': 'error', 'message': "Data doesn't exist"}), 400
