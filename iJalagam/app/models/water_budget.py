from iJalagam.app.models import Block, CensusData, CropCensus, GroundwaterExtraction, LivestockCensus, RainfallDatum, StrangeRunoff, WaterbodyCensus
# from app.models.census_data import CensusData
# from app.models.coefficients import Coefficient
# from app.models.crop_census import CropCensus
# from app.models.groundwater_extraction import GroundwaterExtraction
# from app.models.livestock_census import LivestockCensus
# from app.models.rainfall import RainfallDatum
# from app.models.strange_table import StrangeRunoff
# from app.models.waterbody_census import WaterbodyCensus


class WaterBudget:
    NUMBER_OF_DAYS = 365 # Number of days in a year 
    DECADAL_GROWTH = 1.25 # Decadal growth @ of 25%
    RURAL_CONSUMPTION = 55 # Human consumption of water in rural areas in Litres
    URBAN_CONSUMPTION = 70 # Human consumption of water in urban areas in Litres
    LITRE_TO_HECTARE = 10000000 # Constant for converting hectare to litres

    @classmethod
    def litre_to_hectare_meters(cls, value):
        return value/cls.LITRE_TO_HECTARE

    @classmethod
    def get_human_demand(cls, block_id, district_id):
        human_population = CensusData.get_population_data_by_block(block_id, district_id)
        male_population = human_population['male']
        female_population = human_population['female']
        # divide the consumption by 10000 to convert into hectare meter
        male_consumption = round((int(male_population) * cls.RURAL_CONSUMPTION * cls.DECADAL_GROWTH * cls.NUMBER_OF_DAYS),2)
        female_consumption = round((int(female_population) * cls.RURAL_CONSUMPTION * cls.DECADAL_GROWTH * cls.NUMBER_OF_DAYS),2)

        human = [
            {'name':'male', 'count':round(male_population,2),  # divide by 1000 for population count in thousands
             'consumption': round(cls.litre_to_hectare_meters(male_consumption),2), 'background': 'primary'},
            {'name':'female', 'count':round(female_population,2), 
             'consumption': round(cls.litre_to_hectare_meters(female_consumption),2), 'background': 'danger'},
        ]
        chart_data = [
            {'category':'male', 'value':round(cls.litre_to_hectare_meters(male_consumption),2)}, # divide by 1000 for thousand hecatare meter
            {'category':'female', 'value':round(cls.litre_to_hectare_meters(female_consumption),2)}
        ]
        return human,chart_data
    
    @classmethod
    def get_livestock_demand(cls, block_id, district_id):
        livestocks = LivestockCensus.get_livestock_by_block_id(block_id, district_id)
        backgrounds = ['primary','secondary','success','danger','info','warning']
        # Divide by 10000 to convert to hectare meter
        livestock_data = [{'name': livestock['livestock'], 'count': round(livestock['count'],2), 
                           'consumption': round(cls.litre_to_hectare_meters(livestock['count'] * livestock['coefficient'] * cls.NUMBER_OF_DAYS),2),
                            'background': bg } 
                           for livestock, bg in zip(livestocks, backgrounds)]
        chart_data = [{'name':item['name'], 'value':round(item['consumption'],2)} for item in livestock_data if item['consumption']>0]
        return livestock_data, chart_data

    def get_crops_demand(block_id, district_id):
        crops = CropCensus.get_block_wise_crop(block_id, district_id)
        sorted_crops = sorted(crops,key=lambda x: x['area'],reverse=True)
        crop_data = [{'crop_name': crop['crop_name'], 'crop_area': round(crop['area'],2), 
                      'crop_consumption': round(crop['area'] * crop['crop_coefficient'],2)} 
                      for crop in sorted_crops[:6]]
        backgrounds = ['primary','secondary','success','danger','info','warning']
        image_names = ['crop_' + str(i+1) + '.png' for i in range(6)]
        crop_data = [
                {**cd, 'background': bg, 'content': img} for cd, bg, img in zip(crop_data, backgrounds, image_names)
            ]      
        
        category = [item['crop_name'][:4] for item in crop_data[:5]]
        values = [item['crop_consumption'] for item in crop_data[:5]]
        data= [round((item['crop_consumption']/max(values)) * 90,2) for item in crop_data[:5]]
        chart_data = {'category':category[::-1], 'data':data[::-1]}
        return crop_data, chart_data

    def get_surface_supply(block_id, district_id):
        waterbodies = WaterbodyCensus.get_count_by_block_id(block_id, district_id)
        backgrounds = ['primary','secondary', 'success', 'danger', 'info', 'warning']
        waterbodies = [
                {**wb, 'background': bg} for wb, bg in zip(waterbodies, backgrounds)
            ]
        sorted_waterbodies =  sorted(waterbodies, key=lambda x: x['storage_capacity'])
        chart_data = {'data': [], 'category': []}
        chart_data['data'] = [waterbody['storage_capacity'] for waterbody in sorted_waterbodies]
        chart_data['category'] = [waterbody['waterbody_type'] for waterbody in sorted_waterbodies]
        return waterbodies, sorted_waterbodies, chart_data

    def get_ground_supply(block_id, district_id):
        groundwater_data = GroundwaterExtraction.get_gw_by_block_id(block_id, district_id)
        backgrounds = ['success','primary','info','danger']
        font_awesomes = ['fa-solid fa-cloud-showers-water','fa-solid fa-faucet-drip',
                         'fa-solid fa-arrow-up-from-ground-water','fa-solid fa-arrow-up-from-water-pump']
        filter_names = ['recharge', 'discharge', 'extractable', 'extraction']
        chart_data = []
        for key,value in groundwater_data.items():
            if key.lower() in filter_names:
                data = {'name': key, 'value': value}
                chart_data.append(data)
        gw_data = [
                {**cd, 'background': bg, 'content': fa} for cd, bg, fa in zip(chart_data, backgrounds, font_awesomes)
            ]
        return gw_data, chart_data

    def get_industry_demand():
        pass

    def get_external_supply():
        pass

    def get_rainfall(block_id, district_id):
        monthwise_rainfall = RainfallDatum.get_rainfall_monthwise(district_id)
        actual_monthwise = [round(float(item['actual']),2) for item in monthwise_rainfall]
        normal_monthwise =[round(float(item['normal']),2) for item in monthwise_rainfall]
        months = [f"{item['month'][:3]}-23" for item in monthwise_rainfall]
        chart_data = {'months':months, 'normal': normal_monthwise, 'actual': actual_monthwise}
        total_actual= sum(actual_monthwise)
        total_normal= sum(normal_monthwise)
        rainfall = [
            {'name':'actual', 'precipitation':round(total_actual,2), 'unit':'mm', 'background': 'primary'},
            {'name':'normal', 'precipitation':round(total_normal,2), 'unit':'mm', 'background': 'danger'}
        ]
        return rainfall, monthwise_rainfall,chart_data

    def get_runoff(block_id, district_id):
        rainfall = RainfallDatum.get_rainfall(district_id, 2023)
        if rainfall > 1500:
            rainfall=1500
        runoff = StrangeRunoff.get_runoff_yield(rainfall)
        land_area = CensusData.get_runoff_by_block_id(block_id)
        good =round((land_area['good'] * runoff['good'])/1000,2)
        average = round((land_area['average'] * runoff['average'])/1000,2)
        bad = round((land_area['bad'] * runoff['bad'])/1000, 2)   
        sum_of_all = good + average + bad
        good_percent = round((good/sum_of_all) * 98, 0)
        if good_percent <= 1:
            good_percent = 1
        average_percent = round((average/sum_of_all) * 98, 0)
        if average_percent <= 1:
            average_percent = 1
        bad_percent = round((bad/sum_of_all) * 98,0)
        if bad_percent <= 1:
            bad_percent = 1
        chart_data = [
                {'runoff_type': 'good' ,'percent': good_percent}, 
                {'runoff_type': 'average' ,'percent': average_percent + good_percent}, 
                {'runoff_type': 'bad' ,'percent': bad_percent  + average_percent + good_percent}
                ]
        # chart_data = sorted(chart_data, key=lambda x: x['percent'], reverse=False)
        runoffs = [
            {'name': 'good', 'value':good, 'background': 'success'},
            {'name': 'average', 'value':average, 'background': 'info'},
            {'name': 'bad', 'value':bad, 'background': 'danger'}
        ]
        catchments = [
            {'name': 'good', 'area':land_area['good'], 'percent_runoff': good_percent, 'runoff':good},
            {'name': 'average', 'area':land_area['average'], 'percent_runoff': average_percent, 'runoff':average},
            {'name': 'bad', 'area':land_area['bad'], 'percent_runoff': bad_percent, 'runoff':bad}
        ]
        return runoffs, catchments, chart_data
    
    @classmethod
    def get_total_supply(cls, block_id, district_id):
        waterbodies = WaterbodyCensus.get_count_by_block_id(block_id, district_id)
        surface_supply = sum(item['storage_capacity'] for item in waterbodies)
        groundwater_data = GroundwaterExtraction.get_gw_by_block_id(block_id, district_id)
        ground_supply = groundwater_data['extraction']
        # total_supply = surface_supply + ground_supply
        # supply_side = [{'description': 'Harvested Surface Water', 'value':surface_supply},
        # {'description': 'Extracted Ground Water', 'value':ground_supply},
        # {'description': 'Total Supply', 'value':total_supply}]

        chart_data = {
            'data':[round(surface_supply/1000,2),round(ground_supply/1000,2)],
            'category':['surface','ground']
            }
        supply_side = [
                    {'category': '','value':0,},
                    {'category': 'Surface','value':surface_supply},
                    {'category': 'Ground','value':ground_supply},
                    {'category': '','value':0}
                ]
        return chart_data, supply_side
    
    @classmethod
    def get_total_demand(cls, block_id, district_id):
        # Human
        human_population = CensusData.get_population_data_by_block(block_id, district_id)
        total_population = human_population['male'] + human_population['female'] 
        decadal_population = total_population * cls.DECADAL_GROWTH
        daily_consumption = decadal_population * cls.RURAL_CONSUMPTION
        annual_human_consumption = daily_consumption * cls.NUMBER_OF_DAYS
        # Human water Consumption in Ha M
        human_water_consumption = cls.litre_to_hectare_meters(annual_human_consumption)
        # Livestock
        livestocks = LivestockCensus.get_livestock_by_block_id(block_id, district_id) 
        daily_livestock_consumption = sum(item['count'] * item['coefficient'] for item in livestocks)
        annual_livestock_consumption = daily_livestock_consumption * cls.NUMBER_OF_DAYS
        # Livestock water Consumption in Ha M
        livestock_water_consumption = cls.litre_to_hectare_meters(annual_livestock_consumption)
        # Crops
        crops = CropCensus.get_block_wise_crop(block_id, district_id)
        crop_water_consumption = sum(item['area'] * item['crop_coefficient'] for item in crops)
        # total_demand = human_water_consumption + livestock_water_consumption + crop_water_consumption
        demand_side = [
                {'category': 'Human','value':human_water_consumption,},
                {'category': 'Livestock','value':livestock_water_consumption,},
                {'category': 'Crops','value':crop_water_consumption,},
                {'category': 'Industry','value':0}
            ]
        # demand_side = [{'description': 'Human', 'value':human_water_consumption},
        # {'description': 'Livestock', 'value':livestock_water_consumption},
        # {'description': 'Crops', 'value':crop_water_consumption},
        # {'description': 'Total Demand', 'value':total_demand}]
        # chart_data = {
        #     'data':[
        #         round(human_water_consumption/1000, 2),
        #         round(livestock_water_consumption/1000, 2),
        #         round(crop_water_consumption/1000,2)
        #         ],
        #     'category':['human','livestock','crops']
        #     }
        return demand_side

    def get_session_payload(block_id, district_id, state_id):
        return Block.get_id_and_name(block_id, district_id, state_id)
