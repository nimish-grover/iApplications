from flask import url_for
from sqlalchemy import case, func
from iJalagam.app.db import db
from iJalagam.app.models.block_crops import BlockCrop
from iJalagam.app.models.block_ground import BlockGround
from iJalagam.app.models.block_industries import BlockIndustry
from iJalagam.app.models.block_livestocks import BlockLivestock
from iJalagam.app.models.block_lulc import BlockLULC
from iJalagam.app.models.block_pop import BlockPop
from iJalagam.app.models.block_rainfall import BlockRainfall
from iJalagam.app.models.block_surface import BlockWaterbody
from iJalagam.app.models.block_territory import BlockTerritory
from iJalagam.app.models.block_transfer import BlockWaterTransfer
from iJalagam.app.models.blocks import Block
from iJalagam.app.models.districts import District

class State(db.Model):
    __tablename__ = 'states'
    block_lgd_codes = [4876, 1740, 7130, 539, 172, 3209, 6050, 7047, 3784, 3837, 3979, 4010, 4027, 4628, 624, 762, 781, 2157, 6255, 6287, 6468, 5250, 823, 951, 994]
    district_lgd_codes = [745, 196, 641, 72, 20, 338, 563, 9, 434, 398, 431, 426, 405, 500, 92, 115, 112, 227, 583, 596, 610, 721, 129, 119, 132]
        
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    lgd_code = db.Column(db.Integer, unique=True, nullable=True)
    state_name = db.Column(db.String(255), nullable=True)
    census_code = db.Column(db.Integer, nullable=True)
    is_state = db.Column(db.Boolean, nullable=True, default=True)
    short_name = db.Column(db.String(10), nullable=True)

    def __init__(self, lgd_code, state_name=None, census_code=None, is_state=None, short_name=None):
        self.lgd_code = lgd_code
        self.state_name = state_name
        self.census_code = census_code
        self.is_state = is_state
        self.short_name = short_name

    def __repr__(self):
        return f"<State(id={self.id}, lgd_code={self.lgd_code}, state_name={self.state_name})>"

    def json(self):
        return {
            "id": self.id,
            "lgd_code": self.lgd_code,
            "state_name": self.state_name,
            "census_code": self.census_code,
            "is_state": self.is_state,
            "short_name": self.short_name
        }
    
    @classmethod
    def get_states_by_id(cls, state_id):
        results = cls.query.filter_by(id=state_id).all()
        if results:
            json_data = [{'tj_id':0,'id':item.id,'name':item.state_name,'code':item.lgd_code} for item in results]
            return json_data
        else:
            return None


    @classmethod
    def get_all_states_status(cls):
        filtered_data = db.session.query(
            State.id.label('state_id'),
            State.state_name,
            State.short_name.label('state_short_name'),
            District.id.label('district_id'),
            District.district_name,
            Block.id.label('block_id'),
            Block.block_name,
            Block.lgd_code.label('block_lgd_code'),
            District.lgd_code.label('district_lgd_code'),
            State.lgd_code.label('state_lgd_code')
        ).join(
            District, District.state_lgd_code == State.lgd_code
        ).join(
            Block, Block.district_lgd_code == District.lgd_code
        ).filter(
            Block.lgd_code.in_(cls.block_lgd_codes),
            District.lgd_code.in_(cls.district_lgd_codes)
        ).subquery()

        aggregated_data = db.session.query(
            filtered_data.c.block_id,
            func.coalesce(BlockTerritory.id, 0).label('bt_id'),
            func.max(case((BlockPop.is_approved == 'True', 1), else_=0)).label('population'),
            func.max(case((BlockLivestock.is_approved == 'True', 1), else_=0)).label('livestock'),
            func.max(case((BlockCrop.is_approved == 'True', 1), else_=0)).label('crop'),
            func.max(case((BlockIndustry.is_approved == 'True', 1), else_=0)).label('industry'),
            func.max(case((BlockWaterbody.is_approved == 'True', 1), else_=0)).label('surface'),
            func.max(case((BlockGround.is_approved == 'True', 1), else_=0)).label('ground'),
            func.max(case((BlockLULC.is_approved == 'True', 1), else_=0)).label('lulc'),
            func.max(case((BlockRainfall.is_approved == 'True', 1), else_=0)).label('rainfall'),
            func.max(case((BlockWaterTransfer.is_approved == 'True', 1), else_=0)).label('water_transfer')
        ).outerjoin(
            BlockTerritory, BlockTerritory.block_id == filtered_data.c.block_id
        ).outerjoin(
            BlockPop, BlockPop.bt_id == BlockTerritory.id
        ).outerjoin(
            BlockCrop, BlockCrop.bt_id == BlockTerritory.id
        ).outerjoin(
            BlockLivestock, BlockLivestock.bt_id == BlockTerritory.id
        ).outerjoin(
            BlockIndustry, BlockIndustry.bt_id == BlockTerritory.id
        ).outerjoin(
            BlockWaterbody, BlockWaterbody.bt_id == BlockTerritory.id
        ).outerjoin(
            BlockGround, BlockGround.bt_id == BlockTerritory.id
        ).outerjoin(
            BlockLULC, BlockLULC.bt_id == BlockTerritory.id
        ).outerjoin(
            BlockRainfall, BlockRainfall.bt_id == BlockTerritory.id
        ).outerjoin(
            BlockWaterTransfer, BlockWaterTransfer.bt_id == BlockTerritory.id
        ).group_by(
            filtered_data.c.block_id, BlockTerritory.id
        ).subquery()

        query = db.session.query(
            filtered_data.c.state_name,
            filtered_data.c.state_id,
            filtered_data.c.state_short_name,
            filtered_data.c.district_name,
            filtered_data.c.district_id,
            filtered_data.c.block_name,
            filtered_data.c.block_id,
            aggregated_data.c.bt_id,
            aggregated_data.c.population,
            aggregated_data.c.livestock,
            aggregated_data.c.crop,
            aggregated_data.c.industry,
            aggregated_data.c.surface,
            aggregated_data.c.ground,
            aggregated_data.c.lulc,
            aggregated_data.c.rainfall,
            aggregated_data.c.water_transfer
        ).outerjoin(
            aggregated_data, aggregated_data.c.block_id == filtered_data.c.block_id
        ).order_by(
            filtered_data.c.state_name
        )
        results = query.all()
        results_dict = [row._asdict() for row in results]
        for row in results_dict:
            status_count = 0 
            category = ['population','livestock','crop','industry','surface','ground','lulc','rainfall','water_transfer']
            for item in category:
                if row[item]:
                    status_count += 1
            if status_count < 9 and status_count > 0:
                row['completed'] = 11*status_count
            elif status_count == 9:
                row['completed'] = 100
            else:
                row['completed'] = 0 
            row['url'] = url_for('desktop.human')
        sorted_dict = sorted(results_dict, key=lambda x: x["completed"])
        for idx, item in enumerate(sorted_dict):
            item['id'] = idx + 1
        return sorted_dict
    

