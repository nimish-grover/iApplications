#https://data.desagri.gov.in/website/crops-apy-report-web
from sqlalchemy import func
from iJalagam.app import db
from iJalagam.app.models.blocks import Block 
from iJalagam.app.models.census_data import CensusData
from iJalagam.app.models.crop import Crop
from iJalagam.app.models.districts import District
from iJalagam.app.models.states import State
from iJalagam.app.models.villages import Village


class CropCensus(db.Model):
    __tablename__ = "crop_census"

    # state,district,year,crop_name,crop_season,crop_area,crop_production,crop_yield

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    season = db.Column(db.String(80))
    area = db.Column(db.Float, nullable=False, default=0)
    production = db.Column(db.Float, nullable=False, default=0)
    crop_yield = db.Column(db.Float, nullable=False, default=0)
    census_year = db.Column(db.Integer)
    district_id = db.Column(db.ForeignKey('districts.id'), nullable=False)
    state_id = db.Column(db.ForeignKey('states.id'), nullable=False)
    crop_id = db.Column(db.ForeignKey('crops.id'))

    district = db.relationship('District')
    state = db.relationship('State')
    crop = db.relationship('Crop')

    def __init__(self, name, season, area, production, crop_yield, census_year, district_id, state_id):
        self.name = name
        self.season = season
        self.area = area
        self.production = production
        self.crop_yield = crop_yield
        self.census_year = census_year
        self.district_id = district_id
        self.state_id = state_id

    def json(self):
        return {
            'name': self.name,
            'season': self.season,
            'area': self.area,
            'production': self.production,
            'crop_yield': self.crop_yield,
            'census_year': self.census_year,
            'district_id': self.district_id,
            'state_id': self.state_id
        }
    
    @classmethod
    def get_crops_by_id(cls, _id):
        query = db.session.query(
            cls.name,
            func.sum(cls.area),
            func.sum(cls.production),
            func.sum(cls.crop_yield),
            cls.census_year,
            District.name,
            State.name
        ).join(
            District, District.id == cls.district_id
        ).join(
            State, State.id == cls.state_id
        ).filter(
            cls.district_id == _id
        ).group_by(
            District.name, State.name, cls.name, cls.census_year
        )
    
        results = query.all()

        if results:
            json_data = [{'crop_name': result[0],  
                          'area':result[1], 'production': result[2],
                          'crop_yield': result[3], 'census_year': result[4],
                          'district_name': result[5], 'state_name': result[6]} for result in results]
            return json_data
        else:
            return None
        
    @classmethod
    def get_crops_by_block_id(cls, block_id, district_id):

        # Subquery for total district net sown area
        district_area_subquery = (
            db.session.query(
                CensusData.district_id,
                func.sum(
                    CensusData.unirrigated_area +
                    CensusData.canal_area +
                    CensusData.tubewell_area +
                    CensusData.tank_area +
                    CensusData.waterfall_area +
                    CensusData.other_area
                ).label('total_district_net_sown_area')
            )
            .filter(CensusData.district_id == district_id)
            .group_by(CensusData.district_id)
            .subquery()
        )

        # Main query
        query = (
            db.session.query(
                District.name.label('district_name'),
                Block.id.label('block_id'),
                Block.name.label('block_name'),
                Crop.coefficient.label('crop_coefficient'),
                Crop.name.label('crop_name'),
                (
                    func.sum(
                        (
                            CensusData.unirrigated_area +
                            CensusData.canal_area +
                            CensusData.tubewell_area +
                            CensusData.tank_area +
                            CensusData.waterfall_area +
                            CensusData.other_area
                        ) / district_area_subquery.c.total_district_net_sown_area
                    ) * func.sum(CropCensus.area)
                ).label('village_crop_area')
            )
            .join(Block, District.id == Block.district_id)
            .join(Village, Block.id == Village.block_id)
            .join(CensusData, Village.id == CensusData.village_id)
            .join(CropCensus, District.id == CropCensus.district_id)
            .join(Crop, Crop.id == CropCensus.crop_id)
            .join(district_area_subquery, CensusData.district_id == district_area_subquery.c.district_id)
            .filter(Block.id == block_id)  # Filtering by block_id
            .group_by(District.name, Block.name, Block.id, Crop.name, Crop.coefficient)  # Grouping as per the query
            .order_by(District.name, Block.name)
        )

        
        results =  query.all()

        if results:
            json_data = [{'district_name': result[0], 'block_id':result[1], 
                         'block_name': result[2], 'crop_coefficient':result[3], 
                         'crop_name':result[4], 'area':round(result[5],2)}  
                         for result in results]
            return json_data
        else:
            return None
        
    @classmethod
    def get_block_wise_crop(cls, block_id, district_id):
        # Step 1: Define NetSownArea as a subquery
        net_sown_area_subquery = (
            db.session.query(
                CensusData.state_id,
                CensusData.district_id,
                CensusData.block_id,
                CensusData.village_id,
                func.sum(
                    func.coalesce(CensusData.unirrigated_area, 0) +
                    func.coalesce(CensusData.canal_area, 0) +
                    func.coalesce(CensusData.tubewell_area, 0) +
                    func.coalesce(CensusData.tank_area, 0) +
                    func.coalesce(CensusData.waterfall_area, 0) +
                    func.coalesce(CensusData.other_area, 0)
                ).label("village_net_sown_area")
            )
            .group_by(
                CensusData.state_id,
                CensusData.district_id,
                CensusData.block_id,
                CensusData.village_id
            )
        ).subquery("NetSownArea")

        # Step 2: Define DistrictCropArea as a subquery
        district_crop_area_subquery = (
            db.session.query(
                CropCensus.state_id,
                CropCensus.district_id,
                CropCensus.crop_id,
                func.sum(CropCensus.area).label("total_district_crop_area")
            )
            .filter(CropCensus.district_id == district_id)
            .group_by(
                CropCensus.state_id,
                CropCensus.district_id,
                CropCensus.crop_id
            )
        ).subquery("DistrictCropArea")

        # Step 3: Define VillageCropArea as a subquery with proportional crop area calculation
        village_crop_area_subquery = (
            db.session.query(
                District.state_id.label("state_id"),
                District.id.label("district_id"),
                Block.id.label("block_id"),
                Village.id.label("village_id"),
                Crop.name.label("crop_name"),
                Crop.coefficient.label("crop_coefficient"),
                CropCensus.season,
                CropCensus.crop_id,
                (
                    func.coalesce(net_sown_area_subquery.c.village_net_sown_area, 0) *
                    (
                        district_crop_area_subquery.c.total_district_crop_area /
                        func.nullif(
                            func.sum(net_sown_area_subquery.c.village_net_sown_area)
                            .over(partition_by=[District.id, CropCensus.crop_id]), 
                            0
                        )
                    )
                ).label("village_crop_area")
            )
            .select_from(District)
            .join(Block, District.id == Block.district_id)
            .join(Village, Block.id == Village.block_id)
            .join(CensusData, Village.id == CensusData.village_id)
            .join(CropCensus, District.id == CropCensus.district_id)
            .join(Crop, Crop.id == CropCensus.crop_id)
            .join(net_sown_area_subquery, CensusData.village_id == net_sown_area_subquery.c.village_id)
            .join(district_crop_area_subquery,
                (CropCensus.district_id == district_crop_area_subquery.c.district_id) &
                (CropCensus.crop_id == district_crop_area_subquery.c.crop_id)
            )
        ).subquery("VillageCropArea")

        # Step 4: Final Query
        final_query = (
            db.session.query(
                District.name.label("district_name"),
                Block.id.label("block_id"),
                Block.name.label("block_name"),
                village_crop_area_subquery.c.crop_coefficient,
                village_crop_area_subquery.c.crop_name,
                func.sum(village_crop_area_subquery.c.village_crop_area).label("total_crop_area")
            )
            .select_from(State)
            .join(District, State.id == District.state_id)
            .join(Block, District.id == Block.district_id)
            .join(Village, Block.id == Village.block_id)
            .join(village_crop_area_subquery,
                (village_crop_area_subquery.c.village_id == Village.id) &
                (village_crop_area_subquery.c.block_id == Block.id) &
                (village_crop_area_subquery.c.district_id == District.id) &
                (village_crop_area_subquery.c.state_id == State.id)
            )
            .filter(Block.id == block_id)
            .group_by(
                District.name,
                village_crop_area_subquery.c.crop_name,
                village_crop_area_subquery.c.crop_coefficient,
                Block.id,
                Block.name
            )
            .order_by(
                "crop_name"
            )
        )

        # Execute the query
        results = final_query.all()

        if results:
            json_data = [{'district_name': result[0], 'block_id':result[1], 
                         'block_name': result[2], 'crop_coefficient':result[3], 
                         'crop_name':result[4], 'area':round(result[5],2)}  
                         for result in results]
            return json_data
        else:
            return None
        

