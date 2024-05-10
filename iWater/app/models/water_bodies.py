from iWater.app.db import db
from iWater.app.models.district import District
from iWater.app.models.wb_master import WB_master
from sqlalchemy import func,literal
from iWater.app.models.village import Village
from iWater.app.models.state import State
from iWater.app.models.block import Block

class Water_bodies(db.Model):
    __tablename__ = 'water_bodies'

    id = db.Column(db.Integer, primary_key= True)
    district_code = db.Column(db.Integer)
    village_code = db.Column(db.Integer)
    wb_type_id = db.Column(db.Integer)
    water_spread_area = db.Column(db.Float)
    max_depth = db.Column(db.Float)
    storage_capacity = db.Column(db.Float)
    longitude = db.Column(db.String(80))
    latitude = db.Column(db.String(80))

    
    def __init__(self,district_code,village_code,wb_type_id,water_spread_area,max_depth,storage_capacity,longitude,latitude):
        self.district_code = district_code,
        self.village_code = village_code,
        self.wb_type_id = wb_type_id,
        self.water_spread_area = water_spread_area,
        self.max_depth = max_depth,
        self.storage_capacity = storage_capacity,
        self.longitude = longitude,
        self.latitude = latitude

    
    def json(self):
        return {
            'id': self.id,
            'district_code': self.district_code,
            'village_code' : self.village_code,
            'wb_type_id' : self.wb_type_id,
            'water_spread_area' : self.water_spread_area,
            'max_depth' : self.max_depth,
            'storage_capacity' : self.storage_capacity,
            'longitude' : self.longitude,
            'latitude' : self.latitude
        }
    
    @classmethod
    def get_wb_by_code(cls, _code):
        query=cls.query.filter_by(code=_code).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_wb_by_name(cls, _name):
        query =  cls.query.filter_by(name=_name).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.name)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_code):
        participant = Water_bodies.query.filter_by(code=_code).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_code):
        user = Water_bodies.query.filter_by(code=_code).update(data)
        db.session.commit()
        
        
    @classmethod 
    def bubble_chart_values(cls,json_data={}):
        query = db.session.query(
            func.concat('[', func.to_char(func.sum(Water_bodies.storage_capacity), 'FM999999999.00'), ',',
            func.count(Water_bodies.wb_type_id), ',',
            func.to_char(func.sum(Water_bodies.water_spread_area), 'FM999999999'), ',"',
            District.name, '"]'),
            func.to_char(func.sum(Water_bodies.storage_capacity), 'FM999999999.00').label('storage_capacity'),
            func.count(Water_bodies.wb_type_id).label('count'),
            func.to_char(func.sum(Water_bodies.water_spread_area), 'FM999999999.00').label('spread_area'),
            District.name).\
            join(Village, Village.code == Water_bodies.village_code).\
            join(District, District.id == Village.district_id).\
            join(State, State.code == District.state_id).\
            join(Block, Block.district_id == Water_bodies.district_code).\
            group_by(District.id, District.name).\
            order_by(func.count(Water_bodies.wb_type_id).desc())
                
        if 'state_code' in json_data:
            query = query.filter(State.code == json_data['state_code']).all()
        
        elif 'village_code' in json_data:
            query = query.filter(Village.code == json_data['village_code']).all()
            
        elif 'district_code' in json_data:
            query = query.filter(District.code == json_data['district_code']).all()
            
        elif 'block_code' in json_data:
            query = query.filter(Block.code == json_data['block_code']).all()
            
        else:
            query = query.all()
        return query
        
    """
    select 
    concat('[',
    to_char(sum(water_bodies.storage_capacity),'FM999999999.00'),',',
    count(water_bodies.wb_type_id), ',',
    to_char(sum(water_bodies.water_spread_area),'FM999999999'),',"',
    districts.name,'"','],'),
    count(water_bodies.wb_type_id) as count, 
    to_char(sum(water_bodies.storage_capacity),'FM999999999.00') as storage_capacity,
    to_char(sum(water_bodies.water_spread_area),'FM999999999.00') as spread_area, 
    districts.name
    from water_bodies
    inner join villages on villages.code = water_bodies.village_code
    inner join districts on districts.id = villages.district_id
    inner join states on states.code = districts.state_id
    where districts.state_id = 23
    group by districts.id, districts.name
    order by count(water_bodies.wb_type_id) DESC LIMIT 100
    """
    
    @classmethod
    def doghnut_chart_values(cls,json_data):
        query = db.session.query(
        func.count(Water_bodies.wb_type_id).label('count'),
        WB_master.name).\
        join(WB_master, WB_master.code == Water_bodies.wb_type_id).\
        join(District, District.code == Water_bodies.district_code).\
        join(State, State.code == District.state_id).\
        join(Village, Village.code == Water_bodies.village_code).\
        join(Block, Block.district_id == Water_bodies.district_code).\
        group_by(WB_master.name, WB_master.code).\
        order_by(WB_master.code)
        
        
        if 'state_code' in json_data:
            query = query.filter(State.code == json_data['state_code']).all()
        
        elif 'village_code' in json_data:
            query = query.filter(Village.code == json_data['village_code']).all()
            
        elif 'district_code' in json_data:
            query = query.filter(District.code == json_data['district_code']).all()
        
        elif 'block_code' in json_data:
            query = query.filter(Block.code == json_data['block_code']).all()
        else:
            query = query.all()
        return query
    """
    select count(water_bodies.wb_type_id) as count, wb_master.name as name from water_bodies 
    inner join wb_master on wb_master.code = water_bodies.wb_type_id
    inner join districts on districts.code = water_bodies.district_code
    inner join states on states.code = districts.state_id
    inner join villages on villages.code = water_bodies.village_code
    where states.code=20
    group by wb_master.name, wb_master.code
    order by wb_master.code 
    """
    
    @classmethod
    def get_top_five(cls,json_data):
        if 'district_code' in json_data:
            query = db.session.query(
            State.name.label('state_name'),
            District.name.label('district_name'),
            Block.name.label('block_name'),
            func.count(Water_bodies.id).label('wb_count'),
            func.to_char(func.sum(Water_bodies.storage_capacity), 'FM999999999.00').label('storage_capacity'),
            func.to_char(func.sum(Water_bodies.water_spread_area), 'FM999999999.00').label('spread_area'),
            func.max(Water_bodies.max_depth).label('max_depth')).\
            join(Village, Village.id == Water_bodies.village_code).\
            join(District, District.code == Village.district_id).\
            join(Block, Block.district_id == District.code).\
            join(State, State.id == District.state_id).\
            filter(District.code == json_data['district_code']).\
            group_by(State.name,District.name,Block.id).\
            order_by(func.count(Water_bodies.id).desc()).\
            limit(5).all()
            
        elif 'state_code' in json_data:
            query = db.session.query(
            State.name.label('state_name'),
            District.name.label('district_name'),
            func.count(Water_bodies.id).label('wb_count'),
            func.to_char(func.sum(Water_bodies.storage_capacity), 'FM999999999.00').label('storage_capacity'),
            func.to_char(func.sum(Water_bodies.water_spread_area), 'FM999999999.00').label('spread_area'),
            func.max(Water_bodies.max_depth).label('max_depth')).\
            join(Village, Village.id == Water_bodies.village_code).\
            join(District, District.code == Village.district_id).\
            join(State, State.id == District.state_id).\
            filter(State.code == json_data['state_code']).\
            group_by(State.name,District.id).\
            order_by(func.count(Water_bodies.id).desc()).\
            limit(5).all()
            
        elif 'block_code' in json_data:
            query = db.session.query(
            State.name.label('state_name'),
            District.name.label('district_name'),
            Block.name.label('block_name'),
            Village.name.label('village_name'),
            func.count(Water_bodies.id).label('wb_count'),
            func.to_char(func.sum(Water_bodies.storage_capacity), 'FM999999999.00').label('storage_capacity'),
            func.to_char(func.sum(Water_bodies.water_spread_area), 'FM999999999.00').label('spread_area'),
            func.max(Water_bodies.max_depth).label('max_depth')).\
            join(Village, Village.id == Water_bodies.village_code).\
            join(District, District.code == Village.district_id).\
            join(State, State.id == District.state_id).\
            join(Block, Block.district_id == District.code).\
            filter(Block.code == json_data['block_code']).\
            group_by(State.name,District.name,Block.name,Village.id).\
            order_by(func.count(Water_bodies.id).desc()).\
            limit(5).all()
            
        else:
            query = db.session.query(
            State.name.label('state_name'),
            func.count(Water_bodies.id).label('wb_count'),
            func.to_char(func.sum(Water_bodies.storage_capacity), 'FM999999999.00').label('storage_capacity'),
            func.to_char(func.sum(Water_bodies.water_spread_area), 'FM999999999.00').label('spread_area'),
            func.max(Water_bodies.max_depth).label('max_depth')).\
            join(Village, Village.id == Water_bodies.village_code).\
            join(District, District.code == Village.district_id).\
            join(State, State.id == District.state_id).\
            group_by(State.id).\
            order_by(func.count(Water_bodies.id).desc()).\
            limit(5).all()
            
        return query
    """
    SELECT villages.name district_name, count(water_bodies.id) as wb_count, 
            to_char(SUM(water_bodies.storage_capacity), 'FM999999999.00') AS storage_capacity, 
            to_char(SUM(water_bodies.water_spread_area), 'FM999999999.00') AS spread_area, 
            MAX(water_bodies. max_depth) AS max_depth
            FROM "public"."water_bodies" 
            INNER JOIN villages on villages.id= water_bodies.village_code
            INNER JOIN districts on villages.district_id = districts.code
            inner join blocks on blocks.district_id = districts.code
            INNER JOIN states on states.id = districts.state_id
            where blocks.id = 3742
            GROUP BY villages.id
            ORDER BY wb_count desc LIMIT 100
    """
    
    @classmethod
    def get_count_sum(cls,json_data):
        if 'district_code' in json_data:
            query = db.session.query(
            District.name.label('district_name'),
            func.count(Water_bodies.id).label('wb_count'),
            func.to_char(func.sum(Water_bodies.storage_capacity), 'FM999999999.00').label('storage_capacity'),
            func.to_char(func.sum(Water_bodies.water_spread_area), 'FM999999999.00').label('spread_area')).\
            join(Village, Village.id == Water_bodies.village_code).\
            join(District, District.code == Village.district_id).\
            join(Block, Block.district_id == District.code).\
            join(State, State.id == District.state_id).\
            filter(District.code == json_data['district_code']).\
            group_by(District.id).\
            order_by(func.count(Water_bodies.id).desc()).all()
            
        elif 'village_code' in json_data:
            query = db.session.query(
            Village.name.label('village_name'),
            func.count(Water_bodies.id).label('wb_count'),
            func.to_char(func.sum(Water_bodies.storage_capacity), 'FM999999999.00').label('storage_capacity'),
            func.to_char(func.sum(Water_bodies.water_spread_area), 'FM999999999.00').label('spread_area')).\
            join(Village, Village.id == Water_bodies.village_code).\
            join(District, District.code == Village.district_id).\
            join(State, State.id == District.state_id).\
            filter(Village.code == json_data['village_code']).\
            group_by(Village.name).\
            order_by(func.count(Water_bodies.id).desc()).all()
            
        elif 'state_code' in json_data:
            query = db.session.query(
            State.name.label('state_name'),
            func.count(Water_bodies.id).label('wb_count'),
            func.to_char(func.sum(Water_bodies.storage_capacity), 'FM999999999.00').label('storage_capacity'),
            func.to_char(func.sum(Water_bodies.water_spread_area), 'FM999999999.00').label('spread_area')).\
            join(Village, Village.id == Water_bodies.village_code).\
            join(District, District.code == Village.district_id).\
            join(State, State.id == District.state_id).\
            filter(State.code == json_data['state_name']).\
            group_by(State.name).\
            order_by(func.count(Water_bodies.id).desc()).all()
            
        elif 'block_code' in json_data:
            query = db.session.query(
            Block.name.label('block_name'),
            func.count(Water_bodies.id).label('wb_count'),
            func.to_char(func.sum(Water_bodies.storage_capacity), 'FM999999999.00').label('storage_capacity'),
            func.to_char(func.sum(Water_bodies.water_spread_area), 'FM999999999.00').label('spread_area')).\
            join(Village, Village.id == Water_bodies.village_code).\
            join(District, District.code == Village.district_id).\
            join(State, State.id == District.state_id).\
            join(Block, Block.district_id == District.code).\
            filter(Block.code == json_data['block_code']).\
            group_by(Block.name).\
            order_by(func.count(Water_bodies.id).desc()).all()
            
        else:
            query = db.session.query(
            literal('national').label('name'),
            func.count(Water_bodies.id).label('wb_count'),
            func.to_char(func.sum(Water_bodies.storage_capacity), 'FM999999999.00').label('storage_capacity'),
            func.to_char(func.sum(Water_bodies.water_spread_area), 'FM999999999.00').label('spread_area')).\
            join(Village, Village.id == Water_bodies.village_code).\
            join(District, District.code == Village.district_id).\
            join(State, State.id == District.state_id).\
            order_by(func.count(Water_bodies.id).desc()).all()
            
        return query
    """
    SELECT districts.name state_name, count(water_bodies.id) as wb_count, 
            to_char(SUM(water_bodies.storage_capacity), 'FM999999999.00') AS storage_capacity, 
            to_char(SUM(water_bodies.water_spread_area), 'FM999999999.00') AS spread_area
            FROM "public"."water_bodies" 
            INNER JOIN villages_mp on villages_mp.id= water_bodies.village_code
            INNER JOIN districts on villages_mp.district_id = districts.code
            INNER JOIN states on states.id = districts.state_id
            where districts.code = 410
            GROUP BY districts.id
            ORDER BY wb_count desc
    """
