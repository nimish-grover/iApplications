from itertools import cycle
import os
from flask import current_app, url_for

from iJal.app.models.states import State
from iJal.app.models.villages import Village
from iJal.app.classes.block_or_census import BlockOrCensus
from iJal.app.classes.budget_data import BudgetData
from iJal.app.models.users import User
from iJal.app.models.block_progress import BlockProgress
from iJal.app.classes.new_excel import ExcelGenerator


class HelperClass():
    COLORS = ['#5470c6','#91cc75','#fac858','#ee6666','#73c0de','#3ba272','#fc8452','#9a60b4']

    @classmethod
    def get_dashboard_menu(cls):
        progress_data = BlockProgress.get_all_states_status()
        return progress_data
    
    @classmethod
    def get_card_data(cls,chart_data):
        completed_blocks = sum(1 for item in chart_data if item.get('completed') == 100)
        user_status = User.get_active_count()
        return [
            {'title': 'Users Active', 'value': cls.format_value(user_status['active_users']), 'icon': 'fa-user-gear'},
            {'title': 'Users Registered', 'value': cls.format_value(user_status['active_users']+user_status['inactive_users']), 'icon': 'fa-user-check'},
            {'title': 'Blocks In-Progress', 'value': cls.format_value(len(chart_data)-completed_blocks), 'icon': 'fa-gears'},
            {'title': 'Blocks Completed', 'value': cls.format_value(completed_blocks), 'icon': 'fa-list-check'}]
    
    @classmethod
    def get_print_data(cls,payload):
        
        village_count = Village.get_villages_number_by_block(payload['block_id'],payload['district_id'])
        tga = BlockOrCensus.get_tga(payload['block_id'],payload['district_id'],payload['state_id'])
        basic_info = {"State Name":payload['state_name'],"District Name":payload['district_name'],"Block Name":payload['block_name'],"Village Count":village_count,"TGA":round(tga,2)}
        
        human,is_approved = BlockOrCensus.get_human_data(payload['block_id'],payload['district_id'],payload['state_id'],payload['coefficient'])
        
        livestocks,is_approved = BlockOrCensus.get_livestock_data(payload['block_id'],payload['district_id'],payload['state_id'])
        filtered_livestock = [livestock for livestock in livestocks if livestock['count'] > 0]
        
        crops,is_approved = BlockOrCensus.get_crop_data(payload['block_id'],payload['district_id'],payload['state_id'])
        filtered_crops = [crop for crop in crops if crop['count'] > 0]
        
        industries = BudgetData.get_industry_demand(payload['block_id'],payload['district_id'],payload['state_id'])
        filtered_industries = [industries for industries in industries if industries['count'] > 0]
        
        surface_water,is_approved = BlockOrCensus.get_surface_data(payload['block_id'],payload['district_id'],payload['state_id'])
        filtered_surface_water = [waterbody for waterbody in surface_water if waterbody['count'] > 0]
        surface_rename = {'whs':'WHS','lakes':'Lakes','ponds':'Ponds','tanks':'Tanks','reservoirs':'Resevoirs','others':'Others'}
        filtered_surface_water = [{**item, 'category':surface_rename[item['category']]} for item in filtered_surface_water]

        
        groundwater,is_approved = BlockOrCensus.get_ground_data(payload['block_id'],payload['district_id'],payload['state_id']) 
        groundwater_rename = {'extraction':'Extracted Groundwater','extractable':'Extractable Groundwater','stage_of_extraction':'Stage of Extraction','category':'Category'}
        groundwater = [{**item, 'name':groundwater_rename[item['name']]} for item in groundwater]
        
        water_transfer = BudgetData.get_water_transfer(payload['block_id'],payload['district_id'],payload['state_id'])

        runoff,is_approved = BlockOrCensus.get_runoff_data(payload['block_id'],payload['district_id'],payload['state_id'])
        run_off_rename = {'good':'Good Catchment','bad':'Bad Catchment','average':'Average Catchment'}
        runoff = [{**item, 'catchment':run_off_rename[item['catchment']]} for item in runoff]

        lulc,is_approved = BlockOrCensus.get_lulc_data(payload['block_id'],payload['district_id'],payload['state_id'])
        lulc = [item for item in lulc if item['lulc_name'] != 'TGA']
        
        rainfall,is_approved = BlockOrCensus.get_rainfall_data(payload['block_id'],payload['district_id'],payload['state_id'])
        rainfall_rename = {'Jan':'January','Feb':'February','Mar':'March','Apr':'April','May':'May','Jun':'June','Jul':'July',
                            'Aug':'August','Sep':'September','Oct':'October','Nov':'November','Dec':'December'}
        for item in rainfall:
            month_abbr = item['month'].split('-')[0]
            year = item['month'].split('-')[1]
            full_month_name = rainfall_rename.get(month_abbr, month_abbr)
            item['month'] = f"{full_month_name}-{year}"

        
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
        water_budget_rename = {'demand':'Total Demand','supply':'Total Supply','potential_runoff':'Potential Runoff','harvested_runoff':'Harvested Runoff','available_runoff':'Available Runoff'}
        water_budget = [{**item, 'category':water_budget_rename[item['category']]} for item in water_budget]

        excel_data = {
        'basic_info': basic_info,
        'human_data': human,
        'livestock_data': filtered_livestock,
        'crop_data': filtered_crops,
        'industry_data': filtered_industries,
        'surface_water_data': filtered_surface_water,
        'groundwater_data': groundwater,        
        'transfer_data': water_transfer,
        'runoff_data': runoff,
        'lulc_data': lulc,
        'rainfall_data': rainfall,
        'demand_side': demand_side,
        'supply_side': supply_side,
        'water_budget': water_budget,
        'coefficient': payload.get('coefficient')
        }
        root_path = current_app.root_path
        static_path = "static/assets"
        excel_path = os.path.join(root_path, static_path,'water_budget.xlsx')
        class_obj = ExcelGenerator()
        excel_file = class_obj.create_water_budget_excel(excel_data,excel_path)
        
        return basic_info,human,filtered_livestock,filtered_crops,filtered_industries,filtered_surface_water,groundwater,water_transfer,runoff,lulc,rainfall,demand_side,supply_side,water_budget
        
    def format_value(value):
        if value < 10:
            return f"{value:02d}"
        return str(value)

    def get_supply_menu():
        return [
            { "route" : url_for('.status'), "label":"back", "icon":"fa-solid fa-left-long"},
            { "route" : url_for('.surface'), "label":"surface", "icon":"fa-solid fa-water"},
            { "route" : url_for('.ground'), "label":"ground", "icon":"fa-solid fa-arrow-up-from-ground-water"},
            { "route" : url_for('.lulc'), "label":"lulc", "icon":"fa-solid fa-cloud-showers-water"},
            { "route" : url_for('.rainfall'), "label":"rainfall", "icon":"fa-solid fa-cloud-rain"},
        ]

    def get_demand_menu():
        return [
            { "route" : url_for('.status'), "label":"back", "icon":"fa-solid fa-left-long"},
            { "route" : url_for('.human'), "label":"human", "icon":"fa-solid fa-people-roof"},
            { "route" : url_for('.livestocks'), "label":"livestock", "icon":"fa-solid fa-paw"},
            { "route" : url_for('.crops'), "label":"crops", "icon":"fa-brands fa-pagelines"},
            { "route" : url_for('.industries'), "label":"industries", "icon":"fa-solid fa-industry"},
        ]
    
    def get_main_menu():
        return [
            { "route" : url_for('mobile.index'), "label":"home", "icon":"fa-solid fa-house"},
            { "route" : url_for('desktop.status'), "label":"status", "icon":"fa-solid fa-list-check"},
            { "route" : url_for('desktop.human'), "label":"demand", "icon":"fa-solid fa-chart-line"},
            { "route" : url_for('desktop.surface'), "label":"supply", "icon":"fa-solid fa-glass-water-droplet"},
            { "route" : url_for('desktop.transfer'), "label":"transfer", "icon":"fa-solid fa-arrow-right-arrow-left"},
        ]
    
    def get_admin_menu():
        return [
            { "route" : url_for('.approve'), "label":"approve", "icon":"fa-solid fa-list-check"},
            { "route" : url_for('.dashboard'), "label":"dashboard", "icon":"fa-solid fa-gauge"},
            { "route" : url_for('.progress'), "label":"progress", "icon":"fa-solid fa-bars-progress"},
            { "route" : url_for('.budget'), "label":"budget", "icon":"fa-solid fa-scale-balanced"}
        ]
    
    def get_breadcrumbs(payload):
        """
        Generate breadcrumb navigation based on the current payload.

        Returns:
            list: Breadcrumbs for the current context.
        """
        return [
            {'name': payload['state_name'], 'href': '#'},
            {'name': payload['district_name'], 'href': '#'},
            {'name': payload['block_name'], 'href': '#'}
        ]