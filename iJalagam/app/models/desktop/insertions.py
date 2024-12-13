from . ..models import BlockPopulation,BlockTerritory,BlockLivestock,BlockCrop,BlockIndustry,BlockWaterbody,BlockLulc,BlockRainfall,BlockGroundwater
from . ..models import PopulationCensus,LivestockCensus,CropCensus,WaterbodyCensus,LULCCensus,Rainfall,GroundwaterExtraction,LULC

class Insertion:

    # Block entry insertion in territory
    @classmethod
    def insert_block(cls,payload):
        new_payload = cls.convert_payload(payload)
        record = cls.get_block_territory(new_payload['block_id'])
        if not record:
            row = BlockTerritory(new_payload['state_id'],new_payload['district_id'],new_payload['block_id'])
            row.save_to_db()
            new_record = cls.get_block_territory(new_payload['block_id'])
            if not new_record:
                return None
            return new_record
        return record
    
    @classmethod
    def insert_populations(cls,payload,user_id=1):
        new_payload = cls.convert_payload(payload)
        record = cls.get_block_territory(new_payload['block_id']) 
        if not record:
            record = cls.insert_block(payload)
            territory_id = record['id']
            if not record:
                return {"message":"Cannot insert data in block_territory"}
        territory_id = record['id']
        population_data = BlockPopulation.get_by_territory_id(territory_id)
        if population_data:
            return population_data
        else:
            census_data = PopulationCensus.get_population_by_block(new_payload['block_id'],new_payload['district_id'])
            if census_data:
                insert_census = []
                for data in census_data:
                    class_object = BlockPopulation(data['entity_id'],data['entity_value'],territory_id,False,user_id)
                    insert_census.append(class_object)
                    
                BlockPopulation.save_multiple_to_db(insert_census)
                new_record = BlockPopulation.get_by_territory_id(territory_id)
                if new_record:
                    return new_record
                return {"message":"Cannot insert data in block_populations"}
            return {"messgae":"No data in census table for this block"}

    @classmethod
    def insert_livestocks(cls,payload,user_id=1):
        new_payload = cls.convert_payload(payload)
        record = cls.get_block_territory(new_payload['block_id']) 
        if not record:
            record = cls.insert_block(payload)
            territory_id = record['id']
            if not record:
                return {"message":"Cannot insert data in block_territory"}
        territory_id = record['id']
        livestock_data = BlockLivestock.get_by_territory_id(territory_id)
        if livestock_data:
            return livestock_data
        else:
            census_data = LivestockCensus.get_livestock_by_block(new_payload['block_id'],new_payload['district_id'])
            if census_data:
                insert_census = []
                for data in census_data:
                    
                    class_object = BlockLivestock(data['entity_id'],data['entity_value'],territory_id,False,user_id)
                    insert_census.append(class_object)
                    
                BlockLivestock.save_multiple_to_db(insert_census)
                new_record = BlockLivestock.get_by_territory_id(territory_id)
                if new_record:
                    return new_record
                return {"message":"Cannot insert data in block_livestocks"}
            return {"messgae":"No data in census table for this block"}
        

    @classmethod
    def insert_crops(cls,payload,user_id=1):
        new_payload = cls.convert_payload(payload)
        record = cls.get_block_territory(new_payload['block_id']) 
        if not record:
            record = cls.insert_block(payload)
            territory_id = record['id']
            if not record:
                return {"message":"Cannot insert data in block_territory"}
        territory_id = record['id']
        crop_data = BlockCrop.get_by_territory_id(territory_id)
        if crop_data:
            return crop_data
        else:
            census_data = CropCensus.get_crops_by_block(new_payload['block_id'],new_payload['district_id'])
            if census_data:
                insert_census = []
                for data in census_data:
                    
                    class_object = BlockCrop(data['entity_id'],data['entity_value'],territory_id,False,user_id)
                    insert_census.append(class_object)
                    
                BlockCrop.save_multiple_to_db(insert_census)
                new_record = BlockCrop.get_by_territory_id(territory_id)
                if new_record:
                    return new_record
                return {"message":"Cannot insert data in block_crops"}
            return {"messgae":"No data in census table for this block"}
    
    @classmethod
    def insert_industries(cls,payload,user_id=1):
        new_payload = cls.convert_payload(payload)
        record = cls.get_block_territory(new_payload['block_id']) 
        if not record:
            record = cls.insert_block(payload)
            territory_id = record['id']
            if not record:
                return {"message":"Cannot insert data in block_territory"}
        territory_id = record['id']
        industry_data = BlockIndustry.get_by_territory_id(territory_id)
        if industry_data:
            return industry_data
        else:
            return None
            # census_data = CropCensus.get_crops_by_block(new_payload['block_id'],new_payload['district_id'])
            # if census_data:
            #     insert_census = []
            #     for data in census_data:
                    
            #         class_object = BlockIndustry(data['entity_id'],data['entity_value'],territory_id,False,user_id)
            #         insert_census.append(class_object)
                    
            #     BlockIndustry.save_multiple_to_db(insert_census)
            #     new_record = BlockIndustry.get_by_territory_id(territory_id)
            #     if new_record:
            #         return new_record
                # return {"message":"Cannot insert data in block_livestocks"}
    
    @classmethod
    def insert_surface(cls,payload,user_id=1):
        new_payload = cls.convert_payload(payload)
        record = cls.get_block_territory(new_payload['block_id']) 
        if not record:
            record = cls.insert_block(payload)
            territory_id = record['id']
            if not record:
                return {"message":"Cannot insert data in block_territory"}
        territory_id = record['id']
        surface = BlockWaterbody.get_by_territory_id(territory_id)
        if surface:
            return surface
        else:
            census_data = WaterbodyCensus.get_waterbody_by_block(new_payload['block_id'],new_payload['district_id'])
            if census_data:
                insert_census = []
                for data in census_data:
                    
                    class_object = BlockWaterbody(data['entity_id'],data['entity_count'],data['entity_value'],territory_id,False,user_id)
                    insert_census.append(class_object)
                    
                BlockWaterbody.save_multiple_to_db(insert_census)
                new_record = BlockWaterbody.get_by_territory_id(territory_id)
                if new_record:
                    return new_record
                return {"message":"Cannot insert data in block_surface"}
            return {"messgae":"No data in census table for this block"}
    
    @classmethod
    def insert_groundwater(cls,payload,user_id=1):
        new_payload = cls.convert_payload(payload)
        record = cls.get_block_territory(new_payload['block_id']) 
        if not record:
            record = cls.insert_block(payload)
            territory_id = record['id']
            if not record:
                return {"message":"Cannot insert data in block_territory"}
        territory_id = record['id']
        groundwater = BlockGroundwater.get_by_territory_id(territory_id)
        if groundwater:
            return groundwater
        else:
            census_data = GroundwaterExtraction.get_groundwater_by_block(new_payload['block_id'],new_payload['district_id'])
            if census_data:
                insert_census = []
                for data in census_data:
                    
                    class_object = BlockGroundwater(data['extraction'],data['extractable'],data['stage_of_extraction'],data['category'],territory_id,False,user_id)
                    insert_census.append(class_object)
                    
                BlockGroundwater.save_multiple_to_db(insert_census)
                new_record = BlockGroundwater.get_by_territory_id(territory_id)
                if new_record:
                    return new_record
                return {"message":"Cannot insert data in block_groundwater"}
            return {"messgae":"No data in census table for this block"}
    
    @classmethod
    def insert_lulc(cls,payload,user_id=1):
        new_payload = cls.convert_payload(payload)
        record = cls.get_block_territory(new_payload['block_id']) 
        if not record:
            record = cls.insert_block(payload)
            territory_id = record['id']
            if not record:
                return {"message":"Cannot insert data in block_territory"}
        territory_id = record['id']
        groundwater = BlockLulc.get_by_territory_id(territory_id)
        if groundwater:
            return groundwater
        else:
            census_data = LULCCensus.get_area_by_block(new_payload['block_id'],new_payload['district_id'])
            lulc_type = LULC.get_all()
            if census_data:
                insert_census = []
                for data in census_data:
                    class_object = BlockLulc(data['lulc_id'],data['lulc area'],territory_id,False,user_id)
                    insert_census.append(class_object)
                    
                BlockLulc.save_multiple_to_db(insert_census)
                new_record = BlockLulc.get_by_territory_id(territory_id)
                if new_record:
                    return new_record
                return {"message":"Cannot insert data in block_groundwater"}
            return {"messgae":"No data in census table for this block"}
    
    @classmethod
    def insert_rainfall(cls,payload,user_id=1):
        new_payload = cls.convert_payload(payload)
        record = cls.get_block_territory(new_payload['block_id']) 
        if not record:
            record = cls.insert_block(payload)
            territory_id = record['id']
            if not record:
                return {"message":"Cannot insert data in block_territory"}
        territory_id = record['id']
        rainfall = BlockRainfall.get_by_territory_id(territory_id)
        if rainfall:
            return rainfall
        else:
            census_data = Rainfall.get_monthwise_rainfall(new_payload['district_id'])
            if census_data:
                insert_census = []
                for data in census_data:
                    class_object = BlockRainfall(data['normal'],data['actual'],data['month'],territory_id,False,user_id)
                    insert_census.append(class_object)
                    
                BlockRainfall.save_multiple_to_db(insert_census)
                new_record = BlockRainfall.get_by_territory_id(territory_id)
                if new_record:
                    return new_record
                return {"message":"Cannot insert data in block_groundwater"}
            return {"messgae":"No data in census table for this block"}

    #all table insertions
    @classmethod
    def insert_all_fields(cls,payload):
        payload = cls.convert_payload(payload)
        population = cls.insert_populations(payload)
        if not population:
            return None
        return True
    
    
    
    ## Helper FUnctions

    @classmethod
    def get_block_territory(cls,block_id):
        block_data = BlockTerritory.get_by_block_id(block_id)
        return block_data
    
    @classmethod
    def convert_payload(cls,payload):
        new_payload = {'block_id':payload['block']['id'],
                       'district_id':payload['district']['id'],
                       'state_id':payload['state']['id']}
        return new_payload