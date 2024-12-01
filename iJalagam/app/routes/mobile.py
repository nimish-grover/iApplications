import json
from flask import Blueprint, make_response, redirect, render_template, request, session, url_for

from iJalagam.app.models import State, District, Block
from iJalagam.app.models.water_budget import WaterBudget


blp = Blueprint("mobile", "mobile")

@blp.route("/home", methods=['GET','POST'])
def home():
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('routes.index'))
    district = payload['district']
    block = payload['block']
    demand_side = WaterBudget.get_total_demand(block['id'], district['id'])  
    supply_chart_data, supply_side = WaterBudget.get_total_supply(block['id'], district['id']) 
    runoff = WaterBudget.get_runoff(block['id'], district['id']) 
    total_runoff = sum(item['value'] for item in runoff[0])
    demand = sum([item['value'] for item in demand_side])
    supply = sum([item['value'] for item in supply_side])
    water_budget = [{'name':'Demand','consumption':demand, 'background':'success'},
                    {'name':'Supply','consumption':supply, 'background':'danger'}]
    budget_side = [
        {'description':'Deficiency/Surplus', 'value':supply - demand},
        {'description':'Runoff', 'value':total_runoff},
        {'description':'Availability', 'value': total_runoff + (supply - demand)}
    ]
    colors = ['#c278fd','#f98d8d','#9ee56c','#f564ff']
    demand_data = [{
        'category':item['category'],
        'value':round((item['value']/demand) * 100,0), 
        'color':color 
        } for item, color in zip(demand_side, colors)]
    supply_data = [{
        'category':item['category'],
        'value':round((item['value']/supply) * 100,0), 
        'color':color 
        } for item, color in zip(supply_side, colors)]
    total = demand + supply
    # chart_data = {'demand':demand_chart_data, 'supply':supply_chart_data}
    chart_data=  [  
            {
                'title':'TOTAL WATER DEMAND',
                'data':demand_data
            },
            {
                'title':'TOTAL WATER SUPPLY',
                'data': supply_data,
            },
            {
                'title':'WATER BUDGET',
                'data':[
                    {'category': '','value':0,'color':'#c278fd'},
                    {'category': 'Demand','value':round((demand/total)*100,0),'color':'#f98d8d'},
                    {'category': 'Supply','value':round((supply/total) * 100, 0),'color':'#9ee56c'},
                    {'category': '','value':0,'color':'#f564ff'}
                ],
            }
        ]
    return render_template('mobile/home.html',
                           menu=get_main_menu(), 
                           toggle_labels=['chart','table'], 
                           water_budget = water_budget, 
                           chart_data = json.dumps(chart_data),
                           breadcrumbs = get_breadcrumbs(), 
                           demand_side=demand_side, 
                           supply_side = supply_side,
                           budget_side = budget_side
                           )

@blp.route("/components")
def components():
    return render_template("mobile/components.html")

@blp.route("/index", methods=['GET','POST'])
def index():
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
        return json.dumps(url_for('.home'))
    states = State.get_aspirational_states()
    return render_template("mobile/index.html", states=states)

@blp.route("/districts", methods=['POST'])
def districts():
    json_data = request.json
    if json_data is not None:
        state_id = int(json_data['state_id'])
    else:
        return make_response('', 400)
    districts = District.get_aspirational_districts(state_id)
    if districts:
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
    blocks = Block.get_aspirational_blocks(district_id)
    if blocks:
        return blocks
    else:
        return make_response('', 400)

@blp.route("/human")
def human():
    payload = get_payload()
    block = payload['block']
    district = payload['district']
    human, chart_data = WaterBudget.get_human_demand(block['id'], district['id'])
    return render_template("mobile/demand/human.html",
                           toggle_labels=['chart','table'],
                           human = human,
                           chart_data = json.dumps(chart_data),
                           breadcrumbs=get_breadcrumbs(), 
                           menu=get_demand_menu())

@blp.route("/livestocks")
def livestocks():
    payload = get_payload()
    block = payload['block']
    district = payload['district']
    livestocks, chart_data = WaterBudget.get_livestock_demand(block['id'], district['id'])
    return render_template("mobile/demand/livestocks.html",
                           toggle_labels=['chart','table'],
                           livestocks=livestocks,
                           chart_data = json.dumps(chart_data),
                           breadcrumbs=get_breadcrumbs(), 
                           menu=get_demand_menu())

@blp.route("/crops")
def crops():
    payload = get_payload()
    block = payload['block']
    district = payload['district']    
    crop_data, chart_data = WaterBudget.get_crops_demand(block['id'], district['id'])
    return render_template("mobile/demand/crops.html",
                           toggle_labels=['chart','table'],
                           crops = crop_data,
                           chart_data = json.dumps(chart_data),
                           breadcrumbs=get_breadcrumbs(), 
                           menu=get_demand_menu())

@blp.route("/industry")
def industry():
    return render_template("mobile/demand/industry.html",
                           breadcrumbs=get_breadcrumbs(), 
                           menu=get_demand_menu())

@blp.route("/surface")
def surface():
    payload = get_payload()
    block = payload['block']
    district = payload['district'] 
    waterbodies, sorted_waterbodies, chart_data = WaterBudget.get_surface_supply(block['id'], district['id'])
    return render_template("mobile/supply/surface.html", 
                           toggle_labels=['chart','table'],
                           sorted_waterbodies=sorted_waterbodies,
                           chart_data = json.dumps(chart_data),
                           breadcrumbs=get_breadcrumbs(), 
                           menu=get_supply_menu())

@blp.route("/ground")
def ground():
    payload = get_payload()
    block = payload['block']
    district = payload['district'] 
    gw_data, chart_data = WaterBudget.get_ground_supply(block['id'], district['id'])
    return render_template("mobile/supply/ground.html",
                           chart_data=json.dumps(chart_data), 
                           gw_data=gw_data,
                           table_data=chart_data,
                           toggle_labels=['chart','table'],
                           breadcrumbs=get_breadcrumbs(), 
                           menu=get_supply_menu())

@blp.route("/rainfall")
def rainfall():
    payload = get_payload()
    block = payload['block']
    district = payload['district'] 
    rainfall, monthwise_rainfall, chart_data = WaterBudget.get_rainfall(block['id'], district['id'])
    return render_template("mobile/supply/rainfall.html",
                        rainfalls=rainfall, 
                        monthwise_rainfall=monthwise_rainfall,
                        chart_data=json.dumps(chart_data),
                        toggle_labels=['chart','table'],
                        breadcrumbs=get_breadcrumbs(), 
                        menu=get_supply_menu())

@blp.route("/runoff")
def runoff():
    payload = get_payload()
    block = payload['block']
    district = payload['district'] 
    runoffs, catchments, chart_data = WaterBudget.get_runoff(block['id'], district['id'])
    return render_template("mobile/supply/runoff.html",
                            runoffs = runoffs,
                            catchments=catchments,
                            chart_data = json.dumps(chart_data), 
                            toggle_labels=['chart','table'],
                            breadcrumbs=get_breadcrumbs(), 
                            menu=get_supply_menu())

# HELPER FUNCTIONS 
def get_payload():
    if 'payload' in session:
        payload = session['payload']
        return payload
    else:
        return redirect(url_for('.index'))
    
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
        { "route" : url_for('.home'), "label":"back", "icon":"fa-solid fa-left-long"},
        { "route" : url_for('.surface'), "label":"surface", "icon":"fa-solid fa-water"},
        { "route" : url_for('.ground'), "label":"ground", "icon":"fa-solid fa-arrow-up-from-ground-water"},
        { "route" : url_for('.runoff'), "label":"runoff", "icon":"fa-solid fa-cloud-showers-water"},
        { "route" : url_for('.rainfall'), "label":"rainfall", "icon":"fa-solid fa-cloud-rain"},
    ]

def get_demand_menu():
    return [
        { "route" : url_for('.home'), "label":"back", "icon":"fa-solid fa-left-long"},
        { "route" : url_for('.human'), "label":"human", "icon":"fa-solid fa-people-roof"},
        { "route" : url_for('.livestocks'), "label":"livestock", "icon":"fa-solid fa-paw"},
        { "route" : url_for('.crops'), "label":"crops", "icon":"fa-brands fa-pagelines"},
        { "route" : url_for('.industry'), "label":"industry", "icon":"fa-solid fa-industry"},
    ]

def get_main_menu():
    return [
        { "route" : url_for('.human'), "label":"demand", "icon":"fa-solid fa-chart-line"},
        { "route" : url_for('.index'), "label":"home", "icon":"fa-solid fa-house"},
        { "route" : url_for('.surface'), "label":"supply", "icon":"fa-solid fa-glass-water-droplet"},
    ]