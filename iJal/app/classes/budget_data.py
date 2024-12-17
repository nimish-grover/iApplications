from iJal.app.models.crop_census import CropCensus
from iJal.app.models.groundwater_extraction import GroundwaterExtraction
from iJal.app.models.livestocks_census import LivestockCensus
from iJal.app.models.lulc_census import LULCCensus
from iJal.app.models.population_census import PopulationCensus
from iJal.app.models.rainfall import Rainfall
from iJal.app.models.strange_table import StrangeTable
from iJal.app.models.waterbody_census import WaterbodyCensus
from iJal.app.models.blocks import Block
from itertools import cycle


class BudgetData:
    NUMBER_OF_DAYS = 365 # Number of days in a year 
    DECADAL_GROWTH = 1.25 # Decadal growth @ of 25%
    RURAL_CONSUMPTION = 55 # Human consumption of water in rural areas in Litres
    URBAN_CONSUMPTION = 70 # Human consumption of water in urban areas in Litres
    LITRE_TO_HECTARE = 10000000 # Constant for converting hectare to litres

    @classmethod
    def litre_to_hectare_meters(cls, value):
        return value/cls.LITRE_TO_HECTARE
    
    @classmethod
    def get_human_consumption(cls, block_id, district_id):
        block_lgd = Block.get_block_lgd(block_id)
        entity = PopulationCensus.get_block_or_population_census(block_lgd)
        bg_colors=['red','green']
        for item in entity:
            item['entity_consumption'] = round(cls.litre_to_hectare_meters((int(item['entity_value']) * cls.RURAL_CONSUMPTION * cls.DECADAL_GROWTH * cls.NUMBER_OF_DAYS)),2)
        human_consumption = cls.get_entity_consumption(entity, bg_colors)
        return human_consumption
    
    @classmethod
    def get_livestock_consumption(cls, block_id, district_id):
        block_lgd = Block.get_block_lgd(block_id)
        entity = LivestockCensus.get_block_or_livestock_census(block_lgd)
        bg_colors = ['red','green','blue','gray','black','violet']
        for item in entity:
            item['entity_consumption'] = round(cls.litre_to_hectare_meters(float(item['entity_value']) * float(item['coefficient']) * cls.NUMBER_OF_DAYS),2) 
        livestock_consumption = cls.get_entity_consumption(entity, bg_colors)
        return livestock_consumption
    
    @classmethod
    def get_crops_consumption(cls, block_id, district_id):
        block_lgd = Block.get_block_lgd(block_id)
        entity = CropCensus.get_block_or_crops_census(block_lgd)
        for item in entity:
            item['entity_consumption'] = round(float(item['entity_value']) * float(item['coefficient']),2)         
        bg_colors = ['red','green','blue','gray','black','violet']
        crops_consumption = cls.get_entity_consumption(entity, bg_colors)
        sorted_data = sorted(crops_consumption, key=lambda x: x['value'], reverse=True)
        return sorted_data
    
    @classmethod
    def get_surface_supply(cls, block_id, district_id):
        block_lgd = Block.get_block_lgd(block_id)
        entity = WaterbodyCensus.get_block_or_waterbody_census(block_lgd)
        bg_colors = ['red','green','blue','gray','black','violet']
        surface_supply = cls.get_entity_supply(entity, bg_colors)
        sorted_data = sorted(surface_supply, key=lambda x: x['value'], reverse=False)
        return sorted_data
    
    @classmethod
    def get_ground_supply(cls, block_id, district_id):
        block_lgd = Block.get_block_lgd(block_id)
        entity = GroundwaterExtraction.get_block_or_groundwater_extraction(block_lgd)
        gw_array=[]
        for key,value in entity[0].items():
            item = {
                'name': key,
                'value': value
            }
            gw_array.append(item)
        bg_colors = ['red','green','blue','gray','black','violet']
        ground_supply = [{**item, 'background': bg} for item, bg in zip(gw_array, bg_colors)]
        return ground_supply
    
    @classmethod
    def get_runoff(cls, block_id, district_id):
        block_lgd = Block.get_block_lgd(block_id)
        rainfall_in_mm = 820
        runoff_data = StrangeTable.get_runoff_by_rainfall(rainfall_in_mm)
        lulc_data = LULCCensus.get_block_or_lulc_census(block_lgd)
        runoff_array = []
        for key,value in runoff_data[0].items():
            if not key=='rainfall_in_mm':
                catchment_area = [item['catchment_area'] for item in lulc_data if item['catchment'] == key.lower()][0]
                runoff_yield = round((value/10) * rainfall_in_mm, 2)
                catchment_yield = round(catchment_area * runoff_yield/1000,2)
                item = {'catchment': key, 
                        'runoff': value, 
                        'runoff_yield': runoff_yield, 
                        'supply': catchment_yield}
                runoff_array.append(item)
        bg_colors = ['red','green','blue','gray','black','violet']
        runoff = [{**item, 'background': bg} for item, bg in zip(runoff_array, bg_colors)]
        return runoff
    
    @classmethod
    def get_rainfall(cls, block_id, district_id):
        rainfall_data = Rainfall.get_block_or_rainfall_data(block_id,district_id)
        return rainfall_data
    
    @classmethod
    def get_supply_side(cls, block_id, district_id):
        supply_side = []
        surface = cls.get_surface_supply(block_id, district_id)
        total_surface = sum([item['value'] for item in surface])
        ground = cls.get_ground_supply(block_id, district_id)
        total_ground = [item['value'] for item in ground if item['name'] == 'extraction'][0]
        total_supply = total_surface + total_ground
        supply_side.append({'category':'Surface', 'value':round((total_surface*100)/(total_supply),0),'water_value':total_surface})
        supply_side.append({'category':'Ground', 'value':round((total_ground*100)/(total_supply),0),'water_value':total_ground})
        bg_colors = ['red','green','blue','gray','black','violet']
        supply_with_colors = [{**item, 'background': bg} for item, bg in zip(supply_side, bg_colors)]
        return supply_with_colors
    
    @classmethod
    def get_demand_side(cls, block_id, district_id):
        demand_side = []
        human = cls.get_human_consumption(block_id, district_id)
        total_human = round(sum([float(item['value']) for item in human]), 2)
        livestocks = cls.get_livestock_consumption(block_id, district_id)
        total_livestock = round(sum([item['value']for item in livestocks]),2)
        crops = cls.get_crops_consumption(block_id, district_id)
        total_crop = round(sum([item['value'] for item in crops]),2)
        total_demand = total_human + total_livestock + total_crop
        demand_side.append({'category': 'human','value':round((total_human*100)/(total_demand),0),'water_value':total_human})
        demand_side.append({'category': 'livestock','value':round((total_livestock*100)/(total_demand),0),'water_value':total_livestock})
        demand_side.append({'category': 'crop','value':round((total_crop*100)/(total_demand),0),'water_value':total_crop})
        demand_side.append({'category': 'industry','value':0,'water_value':0}) 
        bg_colors = ['red','green','blue','gray','black','violet']
        demand_with_colors = [{**item, 'background': bg} for item, bg in zip(demand_side, bg_colors)]       
        return demand_with_colors
    
    @classmethod
    def get_water_budget(cls, block_id, district_id):
        water_budget = []
        demand_side = cls.get_demand_side(block_id, district_id)
        total_demand = sum([item['water_value'] for item in demand_side])
        supply_side = cls.get_supply_side(block_id, district_id)
        total_supply = sum([item['water_value'] for item in supply_side])
        water_budget.append({'category':'demand', 'value': round((total_demand*100)/(total_demand + total_supply),0),'water_value':total_demand})
        water_budget.append({'category':'supply', 'value': round((total_supply*100)/(total_demand + total_supply),0),'water_value':total_supply})
        bg_colors = ['red','green','blue','gray','black','violet']
        budget_with_colors = [{**item, 'background': bg} for item, bg in zip(water_budget, bg_colors)] 
        return budget_with_colors

    # Common method for all demand/consumption
    @classmethod
    def get_entity_consumption(cls, entity_array, bg_array):
        new_array=[]
        for item in entity_array:
            entity_item =  {'id':0,'category':'', 'count':0.00,'value': 0.00}
            entity_item['category'] = str(item['entity_name']).lower()
            entity_item['count'] = round(item['entity_value'],2)
            entity_item['value'] = round(item['entity_consumption'],2)
            entity_item['id'] = item['entity_id']
            new_array.append(entity_item)
        entity_consumption = [{**item, 'background': bg} for item, bg in zip(new_array, cycle(bg_array))]
        return entity_consumption
    
    @classmethod
    def get_entity_supply(cls, entity_array, bg_array):
        new_array = []
        for item in entity_array:
            entity_item =  {'id':0, 'category':'', 'count':0.00,'value': 0.00}
            entity_item['category'] = str(item['entity_name']).lower()
            entity_item['count'] = round(item['entity_count'],2)
            entity_item['value'] = round(item['entity_value'],2)
            entity_item['id'] = item['entity_id'] 
            new_array.append(entity_item)
        entity_consumption = [{**item, 'background': bg} for item, bg in zip(new_array, bg_array)]   
        return entity_consumption
