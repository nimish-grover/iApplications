from itertools import cycle
from iJalagam.app.classes.block_data import BlockData
from iJalagam.app.classes.budget_data import BudgetData
from iJalagam.app.models.block_crops import BlockCrop
from iJalagam.app.models.block_ground import BlockGround
from iJalagam.app.models.block_livestocks import BlockLivestock
from iJalagam.app.models.block_pop import BlockPop
from iJalagam.app.models.block_rainfall import BlockRainfall
from iJalagam.app.models.block_surface import BlockWaterbody
from iJalagam.app.models.block_lulc import BlockLULC
from iJalagam.app.models.strange_table import StrangeTable
from iJalagam.app.models.block_transfer import BlockWaterTransfer
from iJalagam.app.models.lulc_census import LULCCensus


class BlockOrCensus:
    NUMBER_OF_DAYS = 365 # Number of days in a year 
    DECADAL_GROWTH = 1.25 # Decadal growth @ of 25%
    RURAL_CONSUMPTION = 55 # Human consumption of water in rural areas in Litres
    URBAN_CONSUMPTION = 70 # Human consumption of water in urban areas in Litres
    LITRE_TO_HECTARE = 10000000 # Constant for converting hectare to litres
    COLORS = ['#5470c6','#91cc75','#fac858','#ee6666','#73c0de','#3ba272','#fc8452','#9a60b4']
    
    @classmethod
    def litre_to_hectare_meters(cls, value):
        return value/cls.LITRE_TO_HECTARE

    @classmethod
    def get_human_data(cls, block_id, district_id, state_id):
        #return block data
        bt_id = BlockData.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        if bt_id:
            human = BlockPop.get_block_population_data(bt_id)
            if human: 
                for item in human:
                    item['entity_consumption'] = round(
                        cls.litre_to_hectare_meters(
                        (int(item['entity_count']) * cls.RURAL_CONSUMPTION 
                        * cls.DECADAL_GROWTH * cls.NUMBER_OF_DAYS)),2)
                human_consumption = cls.get_entity_consumption(human, cls.COLORS)
                is_approved = (
                        all(row['is_approved'] for row in human if row['is_approved'] is not None) 
                        and any(row['is_approved'] is not None for row in human)
                    )
                if is_approved:
                    return human_consumption, is_approved           
            # else return budget data
        human_consumption = BudgetData.get_human_consumption(block_id, district_id)
        return human_consumption, False
    
    @classmethod
    def get_livestock_data(cls, block_id, district_id, state_id):
        bt_id = BlockData.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        if bt_id:
            livestocks = BlockLivestock.get_block_livestock_data(bt_id)
            if livestocks:
                for item in livestocks:
                    item['entity_consumption'] = round(cls.litre_to_hectare_meters(
                        float(item['entity_count']) * float(item['coefficient']) 
                        * cls.NUMBER_OF_DAYS),2) 
                is_approved = (
                    all(row['is_approved'] for row in livestocks if row['is_approved'] is not None) 
                    and any(row['is_approved'] is not None for row in livestocks)
                )
                livestock_consumption = cls.get_entity_consumption(livestocks, cls.COLORS)
                if is_approved:
                    return livestock_consumption, is_approved   
        livestock_consumption = BudgetData.get_livestock_consumption(block_id, district_id)
        return livestock_consumption, False
    
    @classmethod
    def get_crop_data(cls, block_id, district_id, state_id):
        bt_id = BlockData.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        if bt_id:
            crops = BlockCrop.get_block_crop_data(bt_id)
            if crops:
                for item in crops:
                    item['entity_consumption'] = round(
                        float(item['entity_count']) * float(item['coefficient']),2)         
                is_approved = (
                    all(row['is_approved'] for row in crops if row['is_approved'] is not None) 
                    and any(row['is_approved'] is not None for row in crops)
                )
                crop_consumption = cls.get_entity_consumption(crops, cls.COLORS)
                if is_approved:
                    return crop_consumption, is_approved 
        crop_consumption = BudgetData.get_crops_consumption(block_id, district_id)
        return crop_consumption, False

    def get_industry_data():
        #return block data
        return ""
    
    @classmethod
    def get_surface_data(cls, block_id, district_id, state_id):
        bt_id = BlockData.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        if bt_id:
            surface_water = BlockWaterbody.get_block_waterbody_data(bt_id)
            if surface_water:
                is_approved = (
                    all(row['is_approved'] for row in surface_water if row['is_approved'] is not None) 
                    and any(row['is_approved'] is not None for row in surface_water)
                )
                surface_water_supply = cls.get_entity_consumption(surface_water, cls.COLORS)
                if is_approved:
                    return surface_water_supply, is_approved
        surface_water_supply = BudgetData.get_surface_supply(block_id, district_id)
        return surface_water_supply, False
        #return block data
        # else return budget data
        # return ""

    @classmethod
    def get_ground_data(cls, block_id, district_id, state_id):
        bt_id = BlockData.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        ground_water_supply = BudgetData.get_ground_supply(block_id, district_id)
        if bt_id:
            ground_water = BlockGround.get_block_groundwater_data(bt_id)
            if ground_water:
                # is_approved = (
                #     all(row['is_approved'] for row in ground_water if row['is_approved'] is not None) 
                #     and any(row['is_approved'] is not None for row in ground_water)
                # )
                for item in ground_water_supply:
                    if item['name'] == 'extraction':
                        item['value'] = ground_water['extraction']

                is_approved = ground_water['is_approved']
                if is_approved:
                    return ground_water_supply, is_approved
        ground_water_supply = BudgetData.get_ground_supply(block_id, district_id)
        return ground_water_supply, False
    
    @classmethod
    def get_runoff_data(cls, block_id, district_id, state_id):  
        bt_id = BlockData.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        rainfall_in_mm = 820
        runoff_data = StrangeTable.get_runoff_by_rainfall(rainfall_in_mm)
        if bt_id:
            lulc_data = BlockLULC.get_block_lulc_data(bt_id)
            if lulc_data:
                is_approved = all(item['is_approved'] for item in lulc_data)
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
                bg_colors = cls.COLORS
                runoff = [{**item, 'background': bg} for item, bg in zip(runoff_array, bg_colors)]
                if is_approved:
                    return runoff, is_approved
        runoff = BudgetData.get_runoff(block_id, district_id)
        return runoff, False
    
    @classmethod
    def get_rainfall_data(cls, block_id, district_id, state_id):
        bt_id = BlockData.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        if bt_id:
            rainfall = BlockRainfall.get_rainfall_data(bt_id)
            if rainfall:
                is_approved = (
                    all(row['is_approved'] for row in rainfall if row['is_approved'] is not None) 
                    and any(row['is_approved'] is not None for row in rainfall)
                )
                if is_approved:
                    return rainfall, is_approved
        rainfall_data = BudgetData.get_rainfall(block_id, district_id)
        return rainfall_data, False
    
    @classmethod
    def get_tga(cls, block_id, district_id, state_id):
        bt_id = BlockData.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        if bt_id:
            lulc_data = BlockLULC.get_block_lulc_data(bt_id)
            if lulc_data:
                is_approved = (
                    all(row['is_approved'] for row in lulc_data if row['is_approved'] is not None) 
                    and any(row['is_approved'] is not None for row in lulc_data)
                )
                if is_approved:
                    return sum(item['catchment_area'] for item in lulc_data)
        
        lulc_data = LULCCensus.get_census_data_lulc(block_id, district_id)
        return sum(item['catchment_area'] for item in lulc_data)
    
    @classmethod
    def get_demand_side_data(cls, block_id, district_id, state_id):
        demand_side = []
        human,is_approved = cls.get_human_data(block_id, district_id,state_id)
        total_human = round(sum([float(item['value']) for item in human]), 2)
        livestocks,is_approved = cls.get_livestock_data(block_id, district_id,state_id)
        total_livestock = round(sum([item['value']for item in livestocks]),2)
        crops,is_approved = cls.get_crop_data(block_id, district_id,state_id)
        total_crop = round(sum([item['value'] for item in crops]),2)
        industry = BudgetData.get_industry_demand(block_id, district_id,state_id)
        total_industry = round(sum([float(item['value']) for item in industry]), 2)
        total_demand = total_human + total_livestock + total_crop + total_industry
        demand_side.append({'category': 'human','value':round((total_human*100)/(total_demand),0),'water_value':total_human})
        demand_side.append({'category': 'livestock','value':round((total_livestock*100)/(total_demand),0),'water_value':total_livestock})
        demand_side.append({'category': 'crop','value':round((total_crop*100)/(total_demand),0),'water_value':total_crop})
        demand_side.append({'category': 'industry','value':round((total_crop*100)/(total_demand),0),'water_value':total_industry}) 
        bg_colors = cls.COLORS
        demand_with_colors = [{**item, 'background': bg} for item, bg in zip(demand_side, bg_colors)]       
        return demand_with_colors

    @classmethod
    def get_supply_side_data(cls,block_id, district_id, state_id):
        supply_side = []
        surface,is_approved = cls.get_surface_data(block_id, district_id,state_id)
        total_surface = sum([item['value'] for item in surface])
        total_ground = 0
        ground,is_approved = cls.get_ground_data(block_id, district_id,state_id)
        if ground:
            total_ground = [item['value'] for item in ground if item['name'] == 'extraction'][0]
        transfer = BudgetData.get_water_transfer(block_id, district_id,state_id)
        total_transfer = sum([item['entity_value'] for item in transfer])
        positive_transfer = 0
        if total_transfer > 0: 
            positive_transfer = total_transfer
        total_supply = total_surface + total_ground + total_transfer
        supply_side.append({'category':'Surface', 'value':round((total_surface*100)/(total_supply),0),'water_value':total_surface})
        supply_side.append({'category':'Ground', 'value':round((total_ground*100)/(total_supply),0),'water_value':total_ground})
        supply_side.append({'category':'Transfer', 'value':round((positive_transfer*100)/(total_supply),0),'water_value':total_transfer})
        bg_colors = cls.COLORS
        supply_with_colors = [{**item, 'background': bg} for item, bg in zip(supply_side, bg_colors)]
        return supply_with_colors
    
    @classmethod
    def get_water_budget_data(cls, block_id, district_id, state_id):
        water_budget = []
        demand_side = cls.get_demand_side_data(block_id, district_id,state_id)
        total_demand = sum([item['water_value'] for item in demand_side])
        supply_side = cls.get_supply_side_data(block_id, district_id, state_id)
        total_supply = sum([item['water_value'] for item in supply_side])
        water_budget.append({'category':'demand', 'value': round((total_demand*100)/(total_demand + total_supply),0),'water_value':total_demand})
        water_budget.append({'category':'supply', 'value': round((total_supply*100)/(total_demand + total_supply),0),'water_value':total_supply})
        bg_colors = cls.COLORS
        budget_with_colors = [{**item, 'background': bg} for item, bg in zip(water_budget, bg_colors)] 
        return budget_with_colors    

    @classmethod
    def get_entity_consumption(cls, entity_array, bg_array):
        new_array=[]
        for item in entity_array:
            entity_item =  {'id':0,'category':'', 'count':0.00,'value': 0.00, 'is_approved':False}
            entity_item['category'] = str(item['entity_name']).lower()
            entity_item['count'] = round(item['entity_count'],2)
            entity_item['value'] = round(item['entity_consumption'],2)
            entity_item['id'] = item['entity_id']
            entity_item['is_approved'] = item['is_approved']
            new_array.append(entity_item)
        entity_consumption = [{**item, 'background': bg} for item, bg in zip(new_array, cycle(bg_array))]
        return entity_consumption