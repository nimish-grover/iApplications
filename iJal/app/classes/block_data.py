from types import SimpleNamespace
from iJal.app.classes.budget_data import BudgetData
from iJal.app.models.block_crops import BlockCrop
from iJal.app.models.block_ground import BlockGround
from iJal.app.models.block_livestocks import BlockLivestock
from iJal.app.models.block_lulc import BlockLULC
from iJal.app.models.block_pop import BlockPop
from iJal.app.models.block_rainfall import BlockRainfall
from iJal.app.models.block_surface import BlockWaterbody
from iJal.app.models.block_territory import BlockTerritory
from datetime import datetime, timezone

from iJal.app.models.industries import Industry
from iJal.app.models.lulc_census import LULCCensus

class BlockData:
    @classmethod
    def get_bt_id(cls, block_id, district_id, state_id):
        bt_id = BlockTerritory.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        if bt_id:
            return bt_id
        else:
            block_territory = BlockTerritory(state_id=state_id, district_id=district_id, block_id=block_id)
            block_territory.save_to_db()
            bt_id = BlockTerritory.get_bt_id(block_id, district_id, state_id)
            return bt_id
        
    @classmethod
    def get_human_consumption(cls, block_id, district_id, state_id, user_id):
        bt_id = cls.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        return cls.get_or_insert_human(block_id, district_id, bt_id, user_id)
      
    def get_or_insert_human(block_id, district_id, bt_id, user_id):
        human = BlockPop.get_by_bt_id(bt_id)
        if human:
            return human
        else:
            human_consumption = BudgetData.get_human_consumption(block_id=block_id, district_id=district_id)
            if human_consumption:
                for item in human_consumption:
                    block_population = BlockPop(
                                        population_id=item['id'],
                                        count=item['count'],
                                        bt_id=bt_id, 
                                        is_approved=False, 
                                        created_by=user_id)
                    block_population.save_to_db()
                human = BlockPop.get_by_bt_id(bt_id)     
                return human

    def update_human(json_data, user_id):
        for item in json_data: 
            id = item['id']
            count = item['count']
            block_pop = BlockPop.get_by_id(id)
            block_pop.count = count
            block_pop.is_approved = True
            block_pop.created_by = user_id
            block_pop.update_db()
        return True
    
    @classmethod
    def get_livestock_consumption(cls, block_id, district_id, state_id, user_id):
        bt_id = cls.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        return cls.get_or_insert_livestock(block_id, district_id, bt_id, user_id)
    
    def get_or_insert_livestock(block_id, district_id, bt_id, user_id):
        livestock = BlockLivestock.get_by_bt_id(bt_id)
        if livestock:
            return livestock
        else:
            livestock_consumption = BudgetData.get_livestock_consumption(block_id=block_id, district_id=district_id)
            if livestock_consumption:
                for item in livestock_consumption:
                    block_livestock = BlockLivestock(
                                livestock_id=item['id'],
                                count=item['count'],
                                bt_id=bt_id,
                                is_approved=False, 
                                created_by=user_id)
                    block_livestock.save_to_db()
                livestock = BlockPop.get_by_bt_id(bt_id)     
                return livestock
    
    def update_livestock(json_data, user_id):
        for item in json_data: 
            id = item['id']
            count = item['count']
            block_livestock = BlockLivestock.get_by_id(id)
            block_livestock.count = count
            block_livestock.is_approved = True
            block_livestock.created_by = user_id
            block_livestock.update_db()
        return True

    @classmethod
    def get_crops_consumption(cls, block_id, district_id, state_id, user_id):
        bt_id = cls.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        return cls.get_or_insert_crops(block_id, district_id, bt_id, user_id)
    
    def get_or_insert_crops(block_id, district_id, bt_id, user_id):
        crops = BlockCrop.get_by_bt_id(bt_id)
        if crops:
            return crops
        else:
            crops_consumption = BudgetData.get_crops_consumption(block_id=block_id, district_id=district_id)
            if crops_consumption:
                for item in crops_consumption:
                    block_crops = BlockCrop(
                                crop_id=item['id'],
                                area=item['count'],
                                bt_id=bt_id,
                                is_approved=False, 
                                created_by=user_id)
                    block_crops.save_to_db()
                crops = BlockCrop.get_by_bt_id(bt_id)     
                return crops
    
    def update_crops(json_data, user_id):
        for item in json_data: 
            id = item['id']
            crop_area = item['crop_area']
            block_crops = BlockCrop.get_by_id(id)
            block_crops.area = crop_area
            block_crops.is_approved = True
            block_crops.created_by = user_id
            block_crops.update_db()
        return True
    
    def get_industries():
        industries = Industry.get_all_industries()
        results =[{'id': item.id, 'category':item.industry_sector } for item in industries]
        return results 
    
    @classmethod
    def get_surface_supply(cls, block_id, district_id, state_id, user_id):
        bt_id = cls.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        return cls.get_or_insert_surface_supply(block_id, district_id, bt_id, user_id)
    
    def get_or_insert_surface_supply(block_id, district_id, bt_id, user_id):
        waterbodies = BlockWaterbody.get_by_bt_id(bt_id)
        if waterbodies:
            return waterbodies
        else:
            surface_supply = BudgetData.get_surface_supply(block_id=block_id, district_id=district_id)
            if surface_supply:
                for item in surface_supply:
                    block_surface = BlockWaterbody(
                        wb_type_id = item['id'],
                        count = item['count'],
                        storage=item['value'],
                        bt_id=bt_id,
                        is_approved=False,
                        created_by=user_id
                    )
                    block_surface.save_to_db()
                waterbodies = BlockWaterbody.get_by_bt_id(bt_id)     
                return waterbodies
    
    def update_surface(json_data, user_id):
        for item in json_data:
            if item:
                id = item['id']
                block_surface = BlockWaterbody.get_by_id(id)
                if block_surface: 
                    block_surface.count = item['count']
                    block_surface.storage = item['storage']
                    block_surface.is_approved = True
                    block_surface.created_by = user_id
                    block_surface.update_db()
        return True

    @classmethod
    def get_groundwater_supply(cls, block_id, district_id, state_id, user_id):
        bt_id = cls.get_bt_id(block_id=block_id, district_id=district_id, state_id=state_id)
        return cls.get_or_insert_groundwater_supply(block_id, district_id, bt_id, user_id)
    
    def get_or_insert_groundwater_supply(block_id, district_id, bt_id, user_id):
        groundwater_supply = BlockGround.get_by_bt_id(bt_id)
        if groundwater_supply:
            return groundwater_supply
        else: 
            groundwater_data = BudgetData.get_ground_supply(block_id, district_id)
            for item in groundwater_data:
                item = SimpleNamespace(**item)
                if item.name.lower() == 'extraction':
                    block_ground = BlockGround(extraction=item.value, 
                                            bt_id=bt_id, 
                                            is_approved=False, 
                                            created_by=user_id)
                    block_ground.save_to_db()
            groundwater_supply = BlockGround.get_by_bt_id(bt_id)
            return groundwater_supply
        
    def update_ground(json_data, user_id):
        for item in json_data: 
            if 'extraction' in item:
                id = item['id']
                block_ground = BlockGround.get_by_id(id)
                block_ground.extraction = item['extraction']
                block_ground.created_by = user_id
                block_ground.is_approved = True
                block_ground.update_db()
        return True
    
    @classmethod
    def get_rainfall_data(cls, block_id, district_id, state_id, user_id):
        bt_id = BlockTerritory.get_bt_id(block_id, district_id, state_id)
        return cls.get_or_insert_rainfall_data(block_id, district_id, bt_id, user_id)
    
    def get_or_insert_rainfall_data(block_id, district_id, bt_id, user_id):
        rainfall = BlockRainfall.get_by_bt_id(bt_id)
        if rainfall:
            return rainfall
        else:
            rainfall_supply = BudgetData.get_rainfall(block_id, district_id)
            if rainfall_supply:
                for item in rainfall_supply:
                    block_rainfall = BlockRainfall(normal=item['normal'],
                                                    actual=item['actual'],
                                                    month_year=datetime.strptime(item['month'], '%b-%y'),
                                                    bt_id=bt_id,
                                                    is_approved=False,
                                                    created_by=user_id)
                    block_rainfall.save_to_db()
                rainfall = BlockRainfall.get_by_bt_id(bt_id) 
                if rainfall:
                    return rainfall
                else:
                    return None
                
    def update_rainfall(json_data, user_id):
        for item in json_data:
            if item:
                id = item['id']
                rainfall = BlockRainfall.get_by_id(id)
                if rainfall:
                    rainfall.actual = item['actual']
                    rainfall.normal = item['normal']
                    rainfall.is_approved = True
                    rainfall.created_by = user_id
                    rainfall.update_db()
        return True
    

    @classmethod
    def get_lulc_supply(cls, block_id, district_id, state_id, user_id):
        bt_id = BlockTerritory.get_bt_id(block_id, district_id, state_id)
        return cls. get_or_insert_lulc(block_id, district_id, bt_id, user_id)

    def get_or_insert_lulc(block_id, district_id, bt_id, user_id):
        lulc = BlockLULC.get_by_bt_id(bt_id)
        if lulc:
            return lulc
        else:
            lulc_supply = LULCCensus.get_lulc(block_id=block_id, district_id=district_id)
            if lulc_supply:
                for item in lulc_supply:
                    block_lulc = BlockLULC(
                        lulc_id=item['lulc_id'],
                        area=item['lulc_area'],
                        bt_id=bt_id,
                        is_approved=False,
                        created_by=user_id)
                    block_lulc.save_to_db()
                lulc = BlockLULC.get_by_bt_id(bt_id)     
                return lulc
            
    def update_lulc(json_data, user_id):
        for item in json_data: 
            id = item['id']
            area = item['area']
            lulc_id = item['lulc_id']
            block_lulc = BlockLULC.get_by_id(id)
            if block_lulc:
                block_lulc.area = area
                block_lulc.lulc_id = lulc_id
                block_lulc.is_approved = True
                block_lulc.created_by = user_id
                block_lulc.update_db()
        return True
    
    
    