from iWater.app.models.crop_area import Crop_area

def agriculture_consumption(json_data):
    area_db = Crop_area.get_crop_area(json_data)
    