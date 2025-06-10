from flask import Blueprint, flash, get_flashed_messages, json, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from iJalagam.app.classes.block_data import BlockData
from iJalagam.app.classes.budget_data import BudgetData
from iJalagam.app.classes.helper import HelperClass
from iJalagam.app.models import BlockTerritory
from iJalagam.app.models.block_pop import BlockPop
from iJalagam.app.classes.block_or_census import BlockOrCensus
from iJalagam.app.models.villages import Village
from iJalagam.app.models.states import State
from iJalagam.app.models.validation_view import ValidationView




blp = Blueprint('desktop','desktop')

# @blp.after_request
# def trigger_refresh_view(response):
#     # Check if the request is for /block or /auth paths
#     if '/block' in request.path:
#         # Run the refresh function in a separate thread to avoid blocking
#         thread = Thread(target=ValidationView.refresh_validation_view())
#         thread.start()
    
#     return response

@blp.route('/status')
def status():
    session_data = session.get('payload')
    if not session_data:
        return redirect(url_for('mobile.index'))
    else:
        payload = json.loads(session_data)
    progress_status = BlockData.get_progress_status(block_id=payload['block_id'], 
                                            district_id=payload['district_id'], 
                                            state_id=payload['state_id'])
    return render_template('desktop/home.html',
                           progress = progress_status,
                           flash_message = get_message(),
                           breadcrumbs=HelperClass.get_breadcrumbs(payload),
                           menu= HelperClass.get_main_menu())


@blp.route('/human', methods=['POST','GET'])
@login_required
def human():
    if request.method=='POST':
        json_data = request.json
        BlockData.update_human(json_data, current_user.id)
        flash('Population Data is Validated/Updated')
        return jsonify({'redirect_url': url_for('.status')})
    session_data = session.get('payload')
    if not session_data:
        return redirect(url_for('mobile.index'))
    else:
        payload = json.loads(session_data)
    human = BlockData.get_human_consumption(block_id=payload['block_id'], 
                                            district_id=payload['district_id'], 
                                            state_id=payload['state_id'],
                                            user_id=current_user.id)
    is_approved = (
        all(row['is_approved'] for row in human if row['is_approved'] is not None) 
        and any(row['is_approved'] is not None for row in human)
    )
    return render_template('desktop/demand/human.html', 
                           human=human, 
                           human_data=json.dumps(human), 
                           is_approved=is_approved,
                           breadcrumbs=HelperClass.get_breadcrumbs(payload),
                           menu= HelperClass.get_demand_menu())

@blp.route('/livestocks', methods=['POST','GET'])
@login_required
def livestocks():
    if request.method=='POST':
        json_data = request.json
        BlockData.update_livestock(json_data, current_user.id)
        flash('Livestock Data is Validated/Updated')
        return jsonify({'redirect_url': url_for('.status')})
    session_data = session.get('payload')
    if not session_data:
        return redirect(url_for('mobile.index'))
    else:
        payload = json.loads(session_data)
    livestocks = BlockData.get_livestock_consumption(block_id=payload['block_id'], 
                                            district_id=payload['district_id'], 
                                            state_id=payload['state_id'],
                                            user_id=current_user.id)
    is_approved = (
        all(row['is_approved'] for row in livestocks if row['is_approved'] is not None) 
        and any(row['is_approved'] is not None for row in livestocks)
    )
    return render_template('desktop/demand/livestock.html', 
                           livestock=livestocks, 
                           livestock_data=json.dumps(livestocks), 
                           is_approved=is_approved,
                           breadcrumbs=HelperClass.get_breadcrumbs(payload),
                           menu= HelperClass.get_demand_menu())

@blp.route('/crops', methods=['POST','GET'])
@login_required
def crops():
    if request.method=='POST':
        json_data = request.json
        BlockData.update_crops(json_data, current_user.id)
        flash('Crops Data is Validated/Updated')
        return jsonify({'redirect_url': url_for('.status')})
    session_data = session.get('payload')
    if not session_data:
        return redirect(url_for('mobile.index'))
    else:
        payload = json.loads(session_data)
    crops = BlockData.get_crops_consumption(block_id=payload['block_id'], 
                                            district_id=payload['district_id'], 
                                            state_id=payload['state_id'],
                                            user_id=current_user.id)
    is_approved = (
        all(row['is_approved'] for row in crops if row['is_approved'] is not None) 
        and any(row['is_approved'] is not None for row in crops)
    )
    return render_template('desktop/demand/crops.html', 
                           crops=crops, 
                           crops_data=json.dumps(crops), 
                           is_approved=is_approved,
                           breadcrumbs=HelperClass.get_breadcrumbs(payload),
                           menu= HelperClass.get_demand_menu())

@blp.route('/industries', methods=['POST','GET'])
@login_required
def industries():
    if request.method=='POST':
        json_data = request.json
        BlockData.update_industries(json_data, current_user.id)
        flash('Industries Data is Validated/Updated')
        return jsonify({'redirect_url': url_for('.status')})
    session_data = session.get('payload')
    if not session_data:
        return redirect(url_for('mobile.index'))
    else:
        payload = json.loads(session_data)
    industries = BlockData.get_block_industries(block_id=payload['block_id'], 
                                            district_id=payload['district_id'], 
                                            state_id=payload['state_id'],
                                            user_id=current_user.id)
    is_approved = (
        all(row['is_approved'] for row in industries if row['is_approved'] is not None) 
        and any(row['is_approved'] is not None for row in industries)
    )
    return render_template('desktop/demand/industry.html', 
                           industries=industries, 
                           industry_data=json.dumps(industries), 
                           is_approved=is_approved,
                           breadcrumbs=HelperClass.get_breadcrumbs(payload),
                           menu= HelperClass.get_demand_menu())

@blp.route('/surface', methods=['POST','GET'])
def surface():
    session_data = session.get('payload')
    if not session_data:
        return redirect(url_for('mobile.index'))
    else:
        payload = json.loads(session_data)
    if request.method=='POST':
        json_data = request.json
        BlockData.update_surface(json_data, current_user.id)
        flash('Surface Water Data is Validated/Updated')
        return jsonify({'redirect_url': url_for('.status')})    
    surface_supply = BlockData.get_surface_supply(block_id=payload['block_id'], 
                                            district_id=payload['district_id'], 
                                            state_id=payload['state_id'],
                                            user_id=current_user.id)
    is_approved = (
        all(row['is_approved'] for row in surface_supply if row['is_approved'] is not None) 
        and any(row['is_approved'] is not None for row in surface_supply)
    )
    return render_template('desktop/supply/surface.html',
                        waterbodies = surface_supply,
                        waterbody_data = json.dumps(surface_supply),
                        is_approved = is_approved,
                        breadcrumbs=HelperClass.get_breadcrumbs(payload),
                        menu= HelperClass.get_supply_menu())

@blp.route('/rainfall', methods=['POST', 'GET'])
def rainfall():
    if request.method=='POST':
        json_data = request.json
        BlockData.update_rainfall(json_data, current_user.id)
        flash('Rainfall Data is Validated/Updated')
        return jsonify({'redirect_url': url_for('.status')})
    session_data = session.get('payload')
    if not session_data:
        return redirect(url_for('mobile.index'))
    else:
        payload = json.loads(session_data)
    rainfall = BlockData.get_rainfall_data(block_id=payload['block_id'], 
                                            district_id=payload['district_id'], 
                                            state_id=payload['state_id'],
                                            user_id=current_user.id)
    
    is_approved = (
        all(row['is_approved'] for row in rainfall if row['is_approved'] is not None) 
        and any(row['is_approved'] is not None for row in rainfall)
    )
    return render_template('desktop/supply/rainfall.html', 
                            rainfall=rainfall, 
                            rainfall_data=json.dumps(rainfall), 
                            is_approved=is_approved,
                            breadcrumbs=HelperClass.get_breadcrumbs(payload),
                            menu= HelperClass.get_supply_menu())

@blp.route('/lulc', methods=['POST', 'GET'])
def lulc():
    if request.method=='POST':
        json_data = request.json
        BlockData.update_lulc(json_data, current_user.id)
        flash('LULC Data is Validated/Updated')
        return jsonify({'redirect_url': url_for('.status')})
    session_data = session.get('payload')
    if not session_data:
        return redirect(url_for('mobile.index'))
    else:
        payload = json.loads(session_data)
    lulc = BlockData.get_lulc_supply(block_id=payload['block_id'], 
                                            district_id=payload['district_id'], 
                                            state_id=payload['state_id'],
                                            user_id=current_user.id)
    is_approved = (
        all(row['is_approved'] for row in lulc if row['is_approved'] is not None) 
        and any(row['is_approved'] is not None for row in lulc)
    )
    return render_template('desktop/supply/lulc.html', 
                        lulc=lulc, 
                        lulc_data=json.dumps(lulc), 
                        is_approved=is_approved,
                        breadcrumbs=HelperClass.get_breadcrumbs(payload),
                        menu= HelperClass.get_supply_menu())

@blp.route('/ground', methods=['POST','GET'])
def ground():
    if request.method=='POST':
        json_data = request.json
        BlockData.update_ground(json_data, current_user.id)
        flash('Ground water Data is Validated/Updated')
        return jsonify({'redirect_url': url_for('.status')})
    session_data = session.get('payload')
    if not session_data:
        return redirect(url_for('mobile.index'))
    else:
        payload = json.loads(session_data)
    ground_supply = BlockData.get_groundwater_supply(block_id=payload['block_id'], 
                                            district_id=payload['district_id'], 
                                            state_id=payload['state_id'],
                                            user_id=current_user.id)
    is_approved = (
        all(row['is_approved'] for row in ground_supply if row['is_approved'] is not None) 
        and any(row['is_approved'] is not None for row in ground_supply)
    )

    return render_template('desktop/supply/ground.html',
                           ground_supply = ground_supply,
                           groundwater_data = json.dumps(ground_supply),
                           is_approved = is_approved,
                           breadcrumbs=HelperClass.get_breadcrumbs(payload),
                           menu= HelperClass.get_supply_menu())

@blp.route('/transfer', methods=["POST",'GET'])
def transfer():
    is_approved=False
    if request.method=='POST':
        json_data = request.json
        BlockData.update_water_transfer(json_data, current_user.id)
        flash('Water Transfer Data is Validated/Updated')
        return jsonify({'redirect_url': url_for('.status')})
    session_data = session.get('payload')
    if not session_data:
        return redirect(url_for('mobile.index'))
    else:
        payload = json.loads(session_data)
    transfer_data = BlockData.get_water_transfer(block_id=payload['block_id'], 
                                            district_id=payload['district_id'], 
                                            state_id=payload['state_id'],
                                            user_id=current_user.id)
    
    is_approved = (
        all(row['is_approved'] for row in transfer_data if row['is_approved'] is not None) 
        and any(row['is_approved'] is not None for row in transfer_data)
    )
    
    return render_template('desktop/transfer.html',
                           water_transfer = transfer_data,
                           transfer_data=json.dumps(transfer_data),
                           is_approved = is_approved,
                           breadcrumbs=HelperClass.get_breadcrumbs(payload),
                           menu= HelperClass.get_main_menu())

@blp.route('/print')
def print():
    session_data = session.get('payload')
    if not session_data:
        return redirect(url_for('mobile.index'))
    else:
        payload = json.loads(session_data)
        
    village_count = Village.get_villages_number_by_block(payload['block_id'],payload['district_id'])
    tga = BlockOrCensus.get_tga(payload['block_id'],payload['district_id'],payload['state_id'])
    
    human,is_approved = BlockOrCensus.get_human_data(payload['block_id'],payload['district_id'],payload['state_id'])
    
    livestocks,is_approved = BlockOrCensus.get_livestock_data(payload['block_id'],payload['district_id'],payload['state_id'])
    filtered_livestock = [livestock for livestock in livestocks if livestock['count'] > 0]
    
    crops,is_approved = BlockOrCensus.get_crop_data(payload['block_id'],payload['district_id'],payload['state_id'])
    filtered_crops = [crop for crop in crops if crop['count'] > 0]
    
    industries = BudgetData.get_industry_demand(payload['block_id'],payload['district_id'],payload['state_id'])
    filtered_industries = [industries for industries in industries if industries['count'] > 0]
    
    surface_water,is_approved = BlockOrCensus.get_surface_data(payload['block_id'],payload['district_id'],payload['state_id'])
    filtered_surface_water = [waterbody for waterbody in surface_water if waterbody['count'] > 0]
    surface_rename = {'whs':'Water Harvesting Structure','lakes':'Lakes','ponds':'Ponds','tanks':'Tanks','reservoirs':'Resevoirs','others':'Others'}
    filtered_surface_water = [{**item, 'category':surface_rename[item['category']]} for item in filtered_surface_water]

    
    groundwater,is_approved = BlockOrCensus.get_ground_data(payload['block_id'],payload['district_id'],payload['state_id']) 
    groundwater_rename = {'extraction':'Extracted Groundwater','extractable':'Extractable Groundwater','stage_of_extraction':'Stage of Extraction','category':'Category'}
    groundwater = [{**item, 'name':groundwater_rename[item['name']]} for item in groundwater]
    
    runoff,is_approved = BlockOrCensus.get_runoff_data(payload['block_id'],payload['district_id'],payload['state_id'])
    run_off_rename = {'good':'Good Catchment','bad':'Bad Catchment','average':'Average Catchment'}
    runoff = [{**item, 'catchment':run_off_rename[item['catchment']]} for item in runoff]
    
    rainfall,is_approved = BlockOrCensus.get_rainfall_data(payload['block_id'],payload['district_id'],payload['state_id'])
    rainfall_rename = {'Jan':'January','Feb':'February','Mar':'March','Apr':'April','May':'May','Jun':'June','Jul':'July',
                        'Aug':'August','Sep':'September','Oct':'October','Nov':'November','Dec':'December'}
    for item in rainfall:
        month_abbr = item['month'].split('-')[0]
        year = item['month'].split('-')[1]
        full_month_name = rainfall_rename.get(month_abbr, month_abbr)
        item['month'] = f"{full_month_name}-{year}"

    water_transfer = BudgetData.get_water_transfer(payload['block_id'],payload['district_id'],payload['state_id'])
    
    demand_side = BlockOrCensus.get_demand_side_data(payload['block_id'],payload['district_id'],payload['state_id'])
    demand_rename = {'human':'Human Population Consumption','livestock':'Livestock Population Consumption'
                        ,'crop':'Crops Consumption','industry':'Industry Consumption'}
    demand_side = [{**item, 'category':demand_rename[item['category']]} for item in demand_side]
    
    supply_side = BlockOrCensus.get_supply_side_data(payload['block_id'],payload['district_id'],payload['state_id'])
    supply_rename = {'Surface':'Available Surface Water','Ground':'Ground Water'}
    for item in supply_side:
        if item['category'] == 'Transfer':
            if item['value'] >0:
                item['category'] = 'Water Transfer Inward'
                transfer_indicator = 'inward'
            else:
                transfer_indicator = 'outward'
                item['category'] = 'Water Transfer Outward'
        else:
            item['category'] = supply_rename[item['category']]
    
    water_budget = BlockOrCensus.get_water_budget_data(payload['block_id'],payload['district_id'],payload['state_id'])
    water_budget_rename = {'demand':'Total Demand','supply':'Total Supply'}
    water_budget = [{**item, 'category':water_budget_rename[item['category']]} for item in water_budget]
    
    return render_template('desktop/print.html',village_count=village_count,tga=round(tga,2),human_data=human,human=json.dumps(human),
                           livestock_data=filtered_livestock,crop_data=filtered_crops,transfer_data = water_transfer,
                           surface_water_data=filtered_surface_water,industry_data=filtered_industries,
                           groundwater_data=groundwater,runoff_data=runoff,rainfall_data=rainfall,transfer_indicator=transfer_indicator,
                           water_budget=water_budget,demand_side=demand_side,supply_side=supply_side,payload=payload)
    


def get_message():
    messages = get_flashed_messages()
    if len(messages) > 0:
        message = messages[0]
    else:
        message = ''

    return message