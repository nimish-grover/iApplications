from flask_smorest import Blueprint
from iWater.app.models.crop_area import Crop_area
from iWater.app.models.crops_type import Crops_type                 
from iWater.app.models.crops import Crops
from flask import jsonify, render_template,request
from iWater.app.routes.water_budget import WaterBudgetCalc


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

@blp.route('/add_crop_data')
def add_crop_data():
    crop_type = Crops_type.get_all()
    states = WaterBudgetCalc.get_states()
    print(crop_type)
    return render_template('add_crop.html',crop_types = crop_type,states = states)

@blp.route('/add_crop_to_db', methods=['POST'])
def add_crop_to_db():
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
    
# @blp.route('/correct_db')
# def correct_db():
#     crop_data = Crop_area(33,22,2,2,1)
#     crop_data.save_to_db()
#     return True