from datetime import datetime
from zoneinfo import ZoneInfo
from iJal.app.db import db
from iJal.app.models.industries import Industry
from sqlalchemy import case, func



class BlockIndustry(db.Model):
    def get_current_time():
        return datetime.now(ZoneInfo('Asia/Kolkata'))
    
    __tablename__ = 'block_industries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    allocation = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer,nullable=False)
    bt_id = db.Column(db.Integer, db.ForeignKey('block_territory.id'), nullable=False)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    created_on = db.Column(db.DateTime, default=get_current_time)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    users = db.relationship('User', backref=db.backref('block_industries', lazy='dynamic'))
    block_territory = db.relationship('BlockTerritory', backref=db.backref('block_industries', lazy='dynamic'))
    industries = db.relationship('Industry', backref=db.backref('block_industries', lazy='dynamic'))
    
    def __init__(self,industry_id,allocation,unit,bt_id,count,is_approved,created_by):
        self.industry_id = industry_id
        self.allocation = allocation
        self.unit = unit
        self.count = count
        self.bt_id = bt_id
        self.is_approved = is_approved
        self.created_by = created_by
        
    def json(self):
        return {
            "id":self.id,
            "industry_id":self.industry_id,
            "unit":self.unit,
            "count":self.count,
            "allocation":self.allocation,
            "is_approved":self.is_approved,
            "bt_id":self.bt_id,
            "created_by":self.created_by,
            "creatd_on":self.created_on
        }
    
    @classmethod
    def get_industries():
        pass
    
    @classmethod
    def get_by_bt_id(cls,bt_id):
        query = (
            db.session.query(
                BlockIndustry.id.label("table_id"),
                Industry.id.label("industry_id"),  # industries.id
                Industry.industry_sector.label("industry_name"),  # industries.industry_sector
                BlockIndustry.bt_id.label("bt_id"),  # block_industries.bt_id
                BlockIndustry.is_approved.label("is_approved"),  # block_industries.is_approved
                func.coalesce(
                    case(
                        (BlockIndustry.bt_id == bt_id, BlockIndustry.allocation),  # CASE WHEN block_industries.bt_id = 1 THEN block_industries.allocation
                        else_=0  # ELSE 0
                    ),
                    0  # COALESCE(..., 0)
                ).label("allocation"),
                func.coalesce(
                    case(
                        (BlockIndustry.bt_id == bt_id, BlockIndustry.count),  # CASE WHEN block_industries.bt_id = 1 THEN block_industries.allocation
                        else_=0  # ELSE 0
                    ),
                    0  # COALESCE(..., 0)
                ).label("count"),
                func.coalesce(
                    case(
                        (BlockIndustry.bt_id == bt_id, BlockIndustry.unit),  # CASE WHEN block_industries.bt_id = 1 THEN block_industries.unit
                        else_=""
                    ),
                    ""  # COALESCE(..., '')
                ).label("unit"),
            )
            .outerjoin(BlockIndustry, Industry.id == BlockIndustry.industry_id)  # LEFT JOIN block_industries ON industries.id = block_industries.industry_id
            .order_by(Industry.id)  # ORDER BY industry_id
        )
        results = query.all()
        
        
        if results:
            json_data = [{'id':index+1,
                          'table_id': getattr(item, 'table_id', 0), 
                          'industry_id':item.industry_id, 
                          'industry_name': item.industry_name, 
                          'is_approved': item.is_approved,
                          'count':item.count,
                          'bt_id':item.bt_id,
                          'unit':item.unit,
                          'allocation':item.allocation} for index,item in enumerate(results)]
            return json_data
        else:
            return None
        
    @classmethod
    def get_by_id(cls,_id):
        return cls.query.filter(cls.id==_id).first()
    
    
    def delete_from_db(object):
        db.session.delete(object)
        db.session.commit()
        
    def update_db(self):
        # db.session.add(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
"""
SELECT industries.id as industry_id,industries.industry_sector as industry_name,block_industries.bt_id ,block_industries.is_approved ,
coalesce(CASE WHEN block_industries.bt_id = 1 THEN block_industries.allocation ELSE 0 end,0) as allocation,
coalesce(CASE WHEN block_industries.bt_id = 1 THEN block_industries.unit ELSE '' end,'') as unit
FROM industries
left join block_industries on industries.id = block_industries.industry_id
order by industry_id 
"""