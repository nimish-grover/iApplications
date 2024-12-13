import json
from flask import Blueprint, make_response, redirect, render_template, request, session, url_for
from iJalagam.app.models.water_budget import WaterBudget
from iJalagam.app.models import LULC,WaterbodyType,Crop,Livestock,Population,State,District,Block,Industry,WaterbodyCensus,GroundwaterExtraction,Rainfall
from iJalagam.app.models.desktop.insertions import Insertion
from iJalagam.app.models import BlockPopulation,BlockLivestock,BlockCrop,BlockIndustry,BlockRainfall,BlockLulc,BlockGroundwater,BlockWaterbody



blp = Blueprint("desktop", "desktop")

@blp.route('/trial')
def trial():
    return render_template('desktop/trial.html')

@blp.route('/select_block',methods=['POST','GET'])
def select_block():
    if request.method == 'POST':
        json_data = request.json
        state_id = json_data['state_id']
        district_id = json_data['district_id']
        block_id = json_data['block_id']
        if block_id:
            payload = WaterBudget.get_session_payload(block_id, district_id, state_id)
        if session is not None:
            session['payload'] = ''
        session['payload'] = payload
        block_insert = Insertion.insert_block(payload)
        if not block_insert:
            return block_insert
        return json.dumps(url_for('.human'))
    states = State.get_aspirational_states()
    for state in states:
        state['name'] = state['state_name']
    return render_template('desktop/index.html',states=states,progress=[])

@blp.route("/districts", methods=['POST'])
def districts():
    json_data = request.json
    if json_data is not None:
        state_id = int(json_data['state_id'])
    else:
        return make_response('', 400)
    state_lgd_code = State.get_lgd_code(state_id)
    districts = District.get_aspirational_districts(state_lgd_code)
    if districts:
        for district in districts:
            district['name'] = district['district_name']
        return districts
    else:
        return make_response('', 400)

@blp.route("/blocks", methods=['POST'])
def blocks():
    json_data = request.json
    if json_data is not None:
        district_id = int(json_data['district_id'])
    else:
        return make_response('', 400)
    district_lgd_code = District.get_lgd_code(district_id)
    blocks = Block.get_aspirational_blocks(district_lgd_code)
    if blocks:
        for block in blocks:
            block['name'] = block['block_name']
        return blocks
    else:
        return make_response('', 400)

@blp.route("/human",methods=['POST','GET'])
def human():
    if request.method == "GET":
        payload = get_payload()
        if not payload:
            return redirect(url_for('.select_block'))

        population_type = Population.get_all()
        dropdown_data = []
    
        for record in population_type:
            temp_dict = {}
            temp_dict['name'] = record['display_name']
            temp_dict['value'] = record['id']
            dropdown_data.append(temp_dict)
        
        human = Insertion.insert_populations(payload)
        for row in human:
            row['name'] = next((item["display_name"] for item in population_type if item["id"] == row["population_id"]),None)
            isApproved = row['isApproved']
        if not human:
            return human
        # progress = {"human":{"isApproved":True,"current":False},"livestock":{"isApproved":True,"current":False},"crop":{"isApproved":False,"current":True},"industry":{"isApproved":False,"current":False}}
        # human, chart_data = WaterBudget.get_human_demand(block['id'], district['id'])
        return render_template("desktop/demand/human.html",
                            progress = get_demand_progress('human'),
                            isApproved = isApproved,
                            human = human,
                            dropdown_data = dropdown_data,
                            breadcrumbs=get_breadcrumbs(),
                            menu=get_demand_menu())
    else:
        updated_data = request.json
        if not updated_data:
            return {"message":"Data not received by server"}
        population_type = Population.get_all()
        db_data = []
        
        for row in updated_data:
            db_dict={}
            row['population_id'] = next((item["id"] for item in population_type if item["display_name"] == row["name"]),None)
            db_dict['id'] = row['db_id']
            db_dict['population_id'] = row['population_id']
            db_dict['count'] = row['count']
            db_dict['b_territory_id'] = row['b_territory_id']
            db_dict['isApproved'] = True
            db_data.append(db_dict)
        BlockPopulation.update_multiple(db_data)
        print(db_data)
        return {"redirect_url":url_for('.human')}

@blp.route("/livestocks",methods=['POST','GET'])
def livestocks():
    if request.method == 'GET':
        payload = get_payload()
        if not payload:
            return redirect(url_for('.select_block'))

        livestock_type = Livestock.get_all()
        dropdown_data = []
    
        for record in livestock_type:
            temp_dict = {}
            temp_dict['name'] = record['livestock_name']
            temp_dict['value'] = record['id']
            dropdown_data.append(temp_dict)
        
        livestocks = Insertion.insert_livestocks(payload)
        for row in livestocks:
            row['name'] = next((item["livestock_name"] for item in livestock_type if item["id"] == row["livestock_id"]),None)
            isApproved = row['isApproved']

        return render_template("desktop/demand/livestocks.html",
                            isApproved = True,
                            progress = get_demand_progress('livestock'),
                            dropdown_data = dropdown_data,
                            livestocks=livestocks,
                            breadcrumbs=get_breadcrumbs(), 
                            menu=get_demand_menu())
    else:
        updated_data = request.json
        if not updated_data:
            return {"message":"Data not received by server"}
        livestock_type = Livestock.get_all()
        db_data = []
        
        for row in updated_data:
            db_dict={}
            row['livestock_id'] = next((item["id"] for item in livestock_type if item["livestock_name"] == row["name"]),None)
            db_dict['id'] = row['db_id']
            db_dict['livestock_id'] = row['livestock_id']
            db_dict['count'] = row['count']
            db_dict['b_territory_id'] = row['b_territory_id']
            db_dict['isApproved'] = True
            db_data.append(db_dict)
        BlockLivestock.update_multiple(db_data)
        print(db_data)
        return {'redirect_url':url_for('.livestocks')}

@blp.route("/crops",methods=['POST','GET'])
def crops():
    if request.method == "GET":
        payload = get_payload()
        if not payload:
            return redirect(url_for('.select_block'))
        
        crop_type = Crop.get_all()
        dropdown_data = []
    
        for record in crop_type:
            temp_dict = {}
            temp_dict['name'] = record['crop_name']
            temp_dict['value'] = record['id']
            dropdown_data.append(temp_dict)
        
        crops= Insertion.insert_crops(payload)
        
        for row in crops:
            row['crop'] = next((item["crop_name"] for item in crop_type if item["id"] == row["crop_id"]),None)
            isApproved = row['isApproved']
            
        return render_template("desktop/demand/crops.html",
                            isApproved = isApproved,
                            progress = get_demand_progress('crop'),
                            crops = crops[:9],
                            dropdown_data = dropdown_data,
                            breadcrumbs=get_breadcrumbs(), 
                            menu=get_demand_menu())
    else:
        updated_data = request.json
        if not updated_data:
            return {"message":"Data not received by server"}
        crop_type = Crop.get_all()
        db_data = []
        
        for row in updated_data:
            db_dict={}
            row['crop_id'] = next((item["id"] for item in crop_type if item["crop_name"] == row["crop"]),None)
            db_dict['id'] = row['db_id']
            db_dict['crop_id'] = row['crop_id']
            db_dict['area'] = row['area']
            db_dict['b_territory_id'] = row['b_territory_id']
            db_dict['isApproved'] = True
            db_data.append(db_dict)
        BlockCrop.update_multiple(db_data)
        print(db_data)
        return {'redirect_url':url_for('.crops')}

@blp.route("/industry",methods=['POST','GET'])
def industry():
    if request.method == "GET":
        payload = get_payload()
        if not payload:
            return redirect(url_for('.select_block'))
        units = [{'value':'CuM','name':'CuM'},{'value':'MLD','name':'MLD'}]
        industry_type = Industry.get_all()
        dropdown_data = []
        for record in industry_type:
            temp_dict = {}
            temp_dict['name'] = record['display_name']
            temp_dict['value'] = record['id']
            dropdown_data.append(temp_dict)
        
        industries = Insertion.insert_industries(payload)
        if not industries:
            industries=[]
            isApproved=False
        else:
            for row in industries:
                row['industry'] = next((item["display_name"] for item in industry_type if item["id"] == row["industry_id"]),None)
                row['unit_value'] = row['unit']
                row['allocation_value'] = row['allocation']
                isApproved = row['isApproved']
            
        return render_template("desktop/demand/industry.html",
                            isApproved = isApproved,
                            progress = get_demand_progress('industry'),
                            units = units,
                            industries = industries,
                            dropdown_data = dropdown_data,
                            breadcrumbs=get_breadcrumbs(), 
                            menu=get_demand_menu())
    else:
        updated_data = request.json
        if not updated_data:
            return {"message":"Data not received by server"}
        industry_type = Industry.get_all()
        db_data = []
        payload = get_payload()
        if not payload:
            return redirect(url_for('.select_block'))
        user_id = 1
        industries_data = Insertion.insert_industries(payload)
        territory_record = Insertion.insert_block(payload)
        b_territory_id = territory_record['id']
        for row in updated_data:
                db_dict={}
                row['industry_id'] = next((item["id"] for item in industry_type if item["display_name"] == row["industry"]),None)
                db_dict['id'] = row['db_id']
                db_dict['industry_id'] = row['industry_id']
                db_dict['allocation'] = row['allocation_value']
                db_dict['unit'] = row['unit_value']
                db_dict['b_territory_id'] = b_territory_id
                db_dict['isApproved'] = True
                db_data.append(db_dict)
        
        if industries_data:
            
            BlockIndustry.update_multiple(db_data)
        else:
            db_objects = []
            for row in db_data:
                object = BlockIndustry(industry_id=row['industry_id'],allocation=row['allocation'],unit=row['unit'],b_territory_id=b_territory_id,isApproved=False,created_by=user_id)
                db_objects.append(object)
                
            BlockIndustry.save_multiple_to_db(db_objects)
            
        return {'redirect_url':url_for('.industry')}

@blp.route("/surface",methods=['POST','GET'])
def surface():
    if request.method == 'GET':
        payload = get_payload()
        if not payload:
            return redirect(url_for('.select_block'))

        waterbody_type = WaterbodyType.get_all()
        dropdown_data = []
    
        for record in waterbody_type:
            temp_dict = {}
            temp_dict['name'] = record['waterbody_name']
            temp_dict['value'] = record['id']
            dropdown_data.append(temp_dict)
            
        waterbodies = Insertion.insert_surface(payload)
        for row in waterbodies:
            row['waterbody'] = next((item["waterbody_name"] for item in waterbody_type if item["id"] == row["wb_type_id"]),None)
            isApproved = row['isApproved']
        
        return render_template("desktop/supply/surface.html", 
                            dropdown_data = dropdown_data,
                            progress = get_supply_progress('surface'),
                            waterbodies=waterbodies,
                            isApproved = isApproved,
                            breadcrumbs=get_breadcrumbs(), 
                            menu=get_supply_menu())
    else:
        updated_data = request.json
        if not updated_data:
            return {"message":"Data not received by server"}
        waterbody_type = WaterbodyType.get_all()
        db_data = []
        
        for row in updated_data:
            db_dict={}
            row['wb_type_id'] = next((item["id"] for item in waterbody_type if item["waterbody_name"] == row["waterbody"]),None)
            db_dict['id'] = row['db_id']
            db_dict['wb_type_id'] = row['wb_type_id']
            db_dict['count'] = row['count']
            db_dict['storage'] = row['storage']
            db_dict['b_territory_id'] = row['b_territory_id']
            db_dict['isApproved'] = True
            db_data.append(db_dict)
        BlockWaterbody.update_multiple(db_data)
        print(db_data)
        return {'redirect_url':url_for('.surface')}

@blp.route("/ground",methods=["POST","GET"])
def ground():
    if request.method == "GET":
        payload = get_payload()
        if not payload:
            return redirect(url_for('.select_block'))
        category = [{'name':'Safe','value':'safe'},{'name':'Semi Critical','value':'semi_crtical'},{'name':'Over Exploited','value':'over_exploited'}]
        gw_data = Insertion.insert_groundwater(payload)
        for row in gw_data:
            isApproved = row['isApproved']
            row['category'] = next((item['name'] for item in category if item['value'] == row['category']), None)

        return render_template("desktop/supply/groundwater.html", 
                            dropdown_data = category,
                            isApproved=isApproved,
                            progress = get_supply_progress('groundwater'),
                            gw_data=gw_data,
                            breadcrumbs=get_breadcrumbs(), 
                            menu=get_supply_menu())
    else:
        updated_data = request.json
        if not updated_data:
            return {"message":"Data not received by server"}
        db_data = []
        category = [{'name':'Safe','value':'safe'},{'name':'Semi Critical','value':'semi_crtical'},{'name':'Over Exploited','value':'over_exploited'}]
        for row in updated_data:
            db_dict={}
            row['category'] = next((item["value"] for item in category if item["name"] == row["category"]),None)
            db_dict['id'] = row['db_id']
            db_dict['category'] = row['category']
            db_dict['extraction'] = row['extraction']
            db_dict['extractable'] = row['extractable']
            db_dict['stage_of_extraction'] = row['stage']
            db_dict['b_territory_id'] = row['b_territory_id']
            db_dict['isApproved'] = True
            db_data.append(db_dict)
        BlockGroundwater.update_multiple(db_data)
        print(db_data)
        return {'redirect_url':url_for('.ground')}

@blp.route("/lulc",methods=['POST','GET'])
def lulc():
    if request.method == 'GET':
        payload = get_payload()
        if not payload:
            return redirect(url_for('.select_block'))
        
        area_type = LULC.get_all()
        dropdown_data = []
    
        for record in area_type:
            temp_dict = {}
            temp_dict['name'] = record['display_name']
            temp_dict['value'] = record['id']
            dropdown_data.append(temp_dict)
        lulc_data = Insertion.insert_lulc(payload)
        for row in lulc_data:
            row['lulc_name'] = next((item["display_name"] for item in area_type if item["id"] == row["lulc_id"]),None)
            isApproved = row['isApproved']
        return render_template("desktop/supply/lulc.html",
                                lulc_data = lulc_data,
                                progress = get_supply_progress('lulc'),
                                isApproved = isApproved,
                                dropdown_data = dropdown_data, 
                                breadcrumbs=get_breadcrumbs(), 
                                menu=get_supply_menu())
    else:
        updated_data = request.json
        if not updated_data:
            return {"message":"Data not received by server"}
        area_type =LULC.get_all()
        db_data = []
        
        for row in updated_data:
            db_dict={}
            row['lulc_id'] = next((item["id"] for item in area_type if item["display_name"] == row["lulc"]),None)
            db_dict['id'] = row['db_id']
            db_dict['lulc_id'] = row['lulc_id']
            db_dict['area'] = row['area']
            db_dict['b_territory_id'] = row['b_territory_id']
            db_dict['isApproved'] = True
            db_data.append(db_dict)
        BlockLulc.update_multiple(db_data)
        print(db_data)
        return {"redirect_url":url_for('.lulc')}


@blp.route("/rainfall",methods=['POST','GET'])
def rainfall():
    if request.method == 'GET':
        payload = get_payload()
        if not payload:
            return redirect(url_for('.select_block'))

        months = [
            {'name': 'January', 'value': 1},
            {'name': 'February', 'value': 2},
            {'name': 'March', 'value': 3},
            {'name': 'April', 'value': 4},
            {'name': 'May', 'value': 5},
            {'name': 'June', 'value': 6},
            {'name': 'July', 'value': 7},
            {'name': 'August', 'value': 8},
            {'name': 'September', 'value': 9},
            {'name': 'October', 'value': 10},
            {'name': 'November', 'value': 11},
            {'name': 'December', 'value': 12},
        ]
        years = [{'name':2023,'value':2023},{'name':2024,'value':2024}]
        rainfall_data = Insertion.insert_rainfall(payload)
        for row in rainfall_data:
            isApproved = row['isApproved']
        
        return render_template("desktop/supply/rainfall.html",
                            isApproved=isApproved,
                            rainfall_data=rainfall_data,
                            progress = get_supply_progress('rainfall'),
                            months = months,
                            years=years,
                            breadcrumbs=get_breadcrumbs(), 
                            menu=get_supply_menu())
    else:
        updated_data = request.json
        print(updated_data)
        return redirect(url_for('.rainfall'))

@blp.route('/approved_status')
def approved_status():
    status = [{'name':'Human','status':False},{'name':'Livestocks','status':True},{'name':'Crops','status':False},{'name':'Industry','status':False},
              {'name':'Surface','status':False},{'name':'Groundwater','status':True},{'name':'LULC','status':False},{'name':'Rainfall','status':False}]
    demand_progress = get_demand_progress()
    supply_progress = get_supply_progress()
    
    progress = demand_progress | supply_progress 
    return render_template('desktop/status.html',status = status)




#### HELPER FUNCTIONS
# HELPER FUNCTIONS 
def get_payload():
    if 'payload' in session:
        payload = session['payload']
        return payload
    else:
        return None
    
    
def get_breadcrumbs():
    payload = get_payload()
    state = payload['state']
    district = payload['district']
    block = payload['block']
    breadcrumbs = [
        {'name': state['name'], 'href': '#'},
        {'name': district['name'], 'href': '#'},
        {'name': block['name'], 'href': '#'},
        ]
    return breadcrumbs

def get_supply_menu():
    return [
        { "route" : url_for('desktop.human'), "label":"Demand", "icon":"fa-solid fa-chart-line"},
        { "route" : url_for('desktop.surface'), "label":"surface", "icon":"fa-solid fa-water"},
        { "route" : url_for('desktop.ground'), "label":"ground", "icon":"fa-solid fa-arrow-up-from-ground-water"},
        { "route" : url_for('desktop.lulc'), "label":"lulc", "icon":"fa-solid fa-cloud-showers-water"},
        { "route" : url_for('desktop.rainfall'), "label":"rainfall", "icon":"fa-solid fa-cloud-rain"},
    ]

def get_demand_progress(name=""):
    human_progress = False
    livestock_progress = True
    crop_progress = False
    industry_progress = False
    data = {'human':[human_progress,'fa-solid fa-people-roof'],
            'livestock':[livestock_progress,'fa-solid fa-paw'],
            'crop':[crop_progress,'fa-brands fa-pagelines'],
            'industry':[industry_progress,'fa-solid fa-industry']}
    
    json_data = {}
    for key,value in data.items():
        if key == name and not value[0]:
            current = True
        else:
            current = False
        json_data[key] = {"isApproved":value[0],"current":current,"icon":value[1]}
        
    return json_data
    
    
def get_supply_progress(name=""):
    surface_progress = False
    rainfall_progress = True
    lulc_progress = False
    groundwater_progress = False
    data = {'surface':[surface_progress,'fa-solid fa-water'],
            'groundwater':[rainfall_progress,'fa-solid fa-arrow-up-from-ground-water'],
            'lulc':[lulc_progress,'fa-solid fa-cloud-showers-water'],
            'rainfall':[groundwater_progress,'fa-solid fa-cloud-rain']}
    
    json_data = {}
    for key,value in data.items():
        if key == name and not value[0]:
            current = True
        else:
            current = False
        json_data[key] = {"isApproved":value[0],"current":current,"icon":value[1]}
        
    return json_data
    
    
    
def get_demand_menu():
    return [
        { "route" : url_for('desktop.surface'), "label":"Supply", "icon":"fa-solid fa-glass-water-droplet"},
        { "route" : url_for('desktop.human'), "label":"human", "icon":"fa-solid fa-people-roof"},
        { "route" : url_for('desktop.livestocks'), "label":"livestock", "icon":"fa-solid fa-paw"},
        { "route" : url_for('desktop.crops'), "label":"crops", "icon":"fa-brands fa-pagelines"},
        { "route" : url_for('desktop.industry'), "label":"industry", "icon":"fa-solid fa-industry"},
    ]
    
def convert_to_dropdown(data):
    dropdown_data = []
    
    for record in data:
        temp_dict = {}
        temp_dict['name'] = record['display_name']
        temp_dict['value'] = record['id']
        dropdown_data.append(temp_dict)
    return dropdown_data
