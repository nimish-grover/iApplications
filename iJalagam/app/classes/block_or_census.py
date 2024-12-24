from itertools import cycle
from iJalagam.app.classes.block_data import BlockData
from iJalagam.app.classes.budget_data import BudgetData
from iJalagam.app.models.block_crops import BlockCrop
from iJalagam.app.models.block_ground import BlockGround
from iJalagam.app.models.block_livestocks import BlockLivestock
from iJalagam.app.models.block_pop import BlockPop
from iJalagam.app.models.block_rainfall import BlockRainfall
from iJalagam.app.models.block_surface import BlockWaterbody


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
    
    def get_runoff_data():
        #return block data
        # else return budget data
        return ""
    
    @classmethod
    def get_rainfall_data(cls, block_id, district_id, state_id):
        bt_id = BlockData.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        if bt_id:
            rainfall = BlockRainfall.get_rainfall_data(bt_id)
            if rainfall:
                return None
        rainfall_data = BudgetData.get_rainfall(block_id, district_id)
        return rainfall_data
    
    def get_demand_side_data():
        return ''
    
    def get_supply_side_data():
        return ""
    
    def get_water_budget_data():
        return ""
    

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