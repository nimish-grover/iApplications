from datetime import datetime
from flask import Blueprint, current_app, flash, json, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from iJalagam.app.models import ExternalSources, Industry, WaterTransfer
from iJalagam.app.models.water_budget import WaterBudget
from iJalagam.app.routes.routes import get_breadcrumbs


blp=Blueprint("entries","entries")

@blp.route("/budget")
def budget():
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
    # if 'payload' in session:
    #     payload = session['payload']
    # else:
    #     return redirect(url_for('routes.index'))
    # district_id = payload['district_id']
    # block_id = payload['block_id']
    # demand, demand_chart_data, demand_side = WaterBudget.get_total_demand(block_id, district_id)  
    # supply, supply_chart_data, supply_side = WaterBudget.get_total_supply(block_id, district_id) 
    # runoff = WaterBudget.get_runoff(block_id, district_id) 
    # total_runoff = sum(item['value'] for item in runoff[0])
    # water_budget = [{'name':'Demand','consumption':demand, 'background':'danger'},
    #                 {'name':'Supply','consumption':supply, 'background':'success'}]
    # budget_side = [
    #     {'description':'Deficiency/Surplus', 'value':supply - demand},
    #     {'description':'Runoff', 'value': total_runoff},
    #     {'description':'Availability', 'value': total_runoff + (supply - demand)}
    # ]
    # # total = demand + supply
    # chart_data = {
    #     'category':['', 'demand', 'supply',''], 
    #     'data':[
    #         { 'value': 0, 'color': '#ee0011' },
    #         { 'value': round(demand/1000,2), 'color': '#ee0011' },
    #         { 'value': round(supply/1000,2), 'color': '#a9cc00' },
    #         { 'value': 0, 'color': '#ee0011' },
    #     ]}
    return render_template('entries/budget.html', 
                           water_budget = water_budget, 
                           chart_data = json.dumps(chart_data),
                           breadcrumbs = get_breadcrumbs(payload), 
                           demand_side = demand_side, 
                           supply_side = supply_side,
                           budget_side = budget_side)

@login_required
@blp.route("/industry", methods=['POST', 'GET'])
def industry():
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('routes.index'))
    district_id = payload['district_id']
    block_id = payload['block_id']
    if request.method =='POST':
        json_data = request.json
        # fixed_json_data = json_data.replace("'",'"')
        # table_data = json.loads(fixed_json_data)
        for row in json_data:
            industry_name = row['industry']
            annual_allocation = row['allocation']
            measuring_unit = row['unit']
            industry = Industry.get_industry(industry_name, block_id, district_id)
            if industry:
                industry.annual_allocation = annual_allocation
                industry.measuring_unit = measuring_unit
                industry.created_by = current_user.id
                industry.created_on = datetime.now()
                industry.update_to_db()
            else:
                industry = Industry(industry_name, annual_allocation, 
                                    measuring_unit, current_user.id, 
                                    block_id, district_id)
                industry.save_to_db()
        return json.dumps({'redirect_to':url_for('entries.external')})
    return render_template('entries/industry.html', breadcrumbs = get_breadcrumbs(payload))

@blp.route("/external", methods=['POST', 'GET'])
@login_required
def external():
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('routes.index'))
    district_id = payload['district_id']
    block_id = payload['block_id']
    if request.method =='POST':
        json_data = request.json
        for row in json_data:
            source_description = row['source']
            annual_allocation = row['allocation']
            measuring_unit = row['unit']
            external = ExternalSources.get_external_source(source_description, block_id, district_id)
            if external:
                external.annual_allocation = annual_allocation
                external.measuring_unit = measuring_unit
                external.created_by = current_user.id
                external.created_on = datetime.now()
                external.update_to_db()
            else:
                external = ExternalSources(source_description, annual_allocation, measuring_unit, current_user.id, block_id, district_id)
                external.save_to_db()
        return json.dumps({'redirect_to':url_for('entries.transfer')})
    return render_template('entries/external.html', breadcrumbs = get_breadcrumbs(payload))

@blp.route("/transfer", methods=['POST', 'GET'])
@login_required
def transfer():
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('routes.index'))
    block_id = payload['block_id']
    district_id = payload['district_id']
    if request.method =='POST':
        json_data = request.json
        for row in json_data:
            transfer_description = row['transfer']
            annual_allocation = row['allocation']
            measuring_unit = row['unit']
            transfer = WaterTransfer.get_water_transfer(transfer_description,block_id, district_id)
            if transfer: 
                transfer.annual_allocation= annual_allocation
                transfer.measuring_unit = measuring_unit
                transfer.created_by = current_user.id
                transfer.update_to_db()
            else:
                new_transfer = WaterTransfer(transfer_description, annual_allocation, measuring_unit, current_user.id, block_id, district_id)
                new_transfer.save_to_db()
        return json.dumps({'redirect_to':url_for('routes.home')})
    return render_template('entries/transfer.html', breadcrumbs = get_breadcrumbs(payload))

@blp.route("/intro")
@login_required
def intro():
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('routes.index'))
    return render_template('entries/intro.html', breadcrumbs = get_breadcrumbs(payload) )

def get_breadcrumbs(payload):
    breadcrumbs = [
        {'name': payload['state_name'], 'href': '/'},
        {'name': payload['district_name'], 'href': '/'},
        {'name': payload['block_name'], 'href': '/'},
        ]
        
    return breadcrumbs

# {'block_id': 3360, 'block_name': 'Chhaigaon Makhan', 'district_id': 358, 'district_name': 'Khandwa (East Nimar)', 'state_id': 23, 'state_name': 'Madhya Pradesh'}