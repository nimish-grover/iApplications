from flask import Blueprint, json, make_response, redirect, render_template, request, session, url_for
from flask_login import login_required

from iJalagam.app.models import Block, District, State 
from iJalagam.app.models.water_budget import WaterBudget


blp = Blueprint('routes', 'routes')

@blp.route('/index', methods = ['GET', 'POST'])
def index():
    # if request.method == 'POST':
    #     json_data = request.json
    #     state_id = json_data['state_id']
    #     district_id = json_data['district_id']
    #     block_id = json_data['block_id']
    #     if block_id:
    #         payload = WaterBudget.get_session_payload(block_id, district_id, state_id)
    #     if session is not None:
    #         session['payload'] = ''
    #     session['payload'] = payload
    #     return json.dumps(url_for('entries.industry'))
    # states = State.get_states()
    # return render_template('select_block.html', states=states)
    return redirect(url_for('routes.select_block'))

@blp.route("/districts", methods=['POST'])
def districts():
    json_data = request.json
    if json_data is not None:
        state_id = int(json_data['state_id'])
    else:
        return make_response('', 400)
    districts = District.get_districts(state_id)
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
    blocks = Block.get_blocks(district_id)
    if blocks:
        return blocks
    else:
        return make_response('', 400)

# DEMAND SIDE
@blp.route('/human')
def human():
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('routes.index'))
    district_id = payload['district_id']
    block_id = payload['block_id']
    human, chart_data = WaterBudget.get_human_demand(block_id, district_id)
    breadcrumbs = get_breadcrumbs(payload)
    return render_template('demand/human.html', human=human, chart_data = json.dumps(chart_data), breadcrumbs=breadcrumbs)



@blp.route('/livestock')
def livestock():
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('routes.index'))
    district_id = payload['district_id']
    block_id = payload['block_id']
    livestocks, chart_data = WaterBudget.get_livestock_demand(block_id, district_id)
    breadcrumbs = get_breadcrumbs(payload)
    return render_template('demand/livestock.html', livestocks = livestocks, 
                           breadcrumbs = breadcrumbs, chart_data = json.dumps(chart_data))

@blp.route('/crops')
def crops():
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('routes.index'))
    district_id = payload['district_id']
    block_id = payload['block_id']
    crop_data, chart_data = WaterBudget.get_crops_demand(block_id, district_id)
    breadcrumbs = get_breadcrumbs(payload)
    # sorted_json_array = sorted(json_array, key=lambda x: (x['crop_area']), reverse=True)
    return render_template('demand/crop.html', crops = crop_data, 
                           chart_data = json.dumps(chart_data), 
                           breadcrumbs=breadcrumbs)

@blp.route('/industry')
def industry():
    return render_template('demand/industry.html')

# SUPPLY SIDE

@blp.route('/rainfall')
def rainfall():
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('routes.index'))
    district_id = payload['district_id']
    block_id = payload['block_id']
    rainfall, monthwise_rainfall, chart_data = WaterBudget.get_rainfall(block_id, district_id)
    breadcrumbs = get_breadcrumbs(payload)
    return render_template('supply/rainfall.html', 
                           rainfalls=rainfall, breadcrumbs=breadcrumbs, monthwise_rainfall=monthwise_rainfall,
                           chart_data=json.dumps(chart_data))

@blp.route('/surface')
def surface():
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('routes.index'))
    district_id = payload['district_id']
    block_id = payload['block_id']
    waterbodies, sorted_waterbodies, chart_data = WaterBudget.get_surface_supply(block_id, district_id)
    breadcrumbs = get_breadcrumbs(payload=payload)   
    return render_template('supply/harvested.html', waterbodies = waterbodies, 
                           sorted_waterbodies=sorted_waterbodies,
                           breadcrumbs = breadcrumbs, chart_data = json.dumps(chart_data))

@blp.route('/ground')
def ground():
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('routes.index'))
    district_id = payload['district_id']
    block_id = payload['block_id']
    gw_data, chart_data = WaterBudget.get_ground_supply(block_id, district_id)
    breadcrumbs = get_breadcrumbs(payload=payload)
    return render_template('supply/groundwater.html', 
                           chart_data=json.dumps(chart_data), 
                           gw_data=gw_data, table_data=chart_data,  breadcrumbs=breadcrumbs)

@blp.route('/runoff')
def runoff():
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('routes.index'))
    district_id = payload['district_id']
    block_id = payload['block_id']
    runoffs, catchments, chart_data = WaterBudget.get_runoff(block_id, district_id)
    breadcrumbs = get_breadcrumbs(payload)
    return render_template('supply/runoff.html', 
                        runoffs=runoffs, 
                        catchments=catchments, 
                        breadcrumbs=breadcrumbs, 
                        chart_data = json.dumps(chart_data))

@blp.route('/home')
def home():
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('routes.index'))
    district_id = payload['district_id']
    block_id = payload['block_id']
    demand_side = WaterBudget.get_total_demand(block_id, district_id)  
    supply_chart_data, supply_side = WaterBudget.get_total_supply(block_id, district_id) 
    runoff = WaterBudget.get_runoff(block_id, district_id) 
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
                # village counts - villages_by_blocks: 693722, 
                # villages_by_blocks_removed_duplicates: 655931, 
                # villages.csv: 666232
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
    return render_template('budget.html', 
                           water_budget = water_budget, 
                           chart_data = json.dumps(chart_data),
                           breadcrumbs = get_breadcrumbs(payload), 
                           demand_side=demand_side, 
                           supply_side = supply_side,
                           budget_side = budget_side)

@blp.route('/external')
def external():
    return render_template('supply/external.html')


@blp.route("/select_block", methods=['POST', 'GET'])
def select_block():
    if request.method=='POST':
        json_data = request.form.get('block_data')
        fixed_json_data = json_data.replace("'", '"')
        payload_data = json.loads(fixed_json_data)
        session['payload'] = payload_data
        return redirect(url_for('entries.intro'))
    symbol_array = [
        {'category': 'safe', 'symbol': 'green'},
        {'category': 'critical', 'symbol': 'yellow'},
        {'category': 'over_exploited', 'symbol': 'yellow'},
        {'category': 'salinity', 'symbol': 'blue'},
        {'category': 'na', 'symbol': 'blue'}
    ]
    # Create a mapping for category to symbol for quick lookup
    symbol_map = {item['category']: item['symbol'] for item in symbol_array}
    blocks = Block.get_aspirational_blocks()
    blocks_with_symbols = [
        {
            **block,
            'symbol': symbol_map.get(block['category'], 'blue')  # Use 'default' if no matching category
        }
        for block in blocks
    ]
    return render_template('/select_block.html', blocks = blocks_with_symbols)

# HELPER FUNCTIONS 

def get_breadcrumbs(payload):
    breadcrumbs = [
        {'name': payload['state_name'], 'href': '/'},
        {'name': payload['district_name'], 'href': '/'},
        {'name': payload['block_name'], 'href': '/'},
        ]
        
    return breadcrumbs

## LINKS
# DEMAND
# Livestock - https://dahd.nic.in/schemes/programmes/animal-husbandry-statistics
# Crops - https://data.desagri.gov.in/website/crops-apy-report-web
# Census Data - /Users/amar/Library/CloudStorage/OneDrive-DeutscheGesellschaftfürInternationaleZusammenarbeit(GIZ)GmbH/WASCA II/Niti Aayog

# SUPPLY
# Rainfall - https://indiawris.gov.in/wris/#/rainfall
# Groundwater - https://ingres.iith.ac.in/api/gec/getBusinessDataForUserOpen
# Waterbody Data - /Users/amar/Library/CloudStorage/OneDrive-DeutscheGesellschaftfürInternationaleZusammenarbeit(GIZ)GmbH/WASCA II/Niti Aayog
