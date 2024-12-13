from sqlalchemy import and_
from iJalagam.app.db import db
from iJalagam.app.models import District,State


class Block(db.Model):
    __tablename__ = 'blocks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    state_lgd_code = db.Column(db.Integer, nullable=False)  # Note: Not a foreign key in the schema
    district_lgd_code = db.Column(db.Integer, db.ForeignKey('districts.lgd_code'), nullable=False)
    lgd_code = db.Column(db.Integer, nullable=False)
    block_name = db.Column(db.String(255), nullable=True)

    __table_args__ = (
        db.UniqueConstraint('lgd_code', 'district_lgd_code', name='blocks_unique_lgd_code_district_lgd_code'),
    )

    # Relationship to District
    district = db.relationship("District", backref=db.backref("blocks", lazy="dynamic"))

    def __init__(self, state_lgd_code, district_lgd_code, lgd_code, block_name=None):
        self.state_lgd_code = state_lgd_code
        self.district_lgd_code = district_lgd_code
        self.lgd_code = lgd_code
        self.block_name = block_name

    def __repr__(self):
        return f"<Block(id={self.id}, lgd_code={self.lgd_code}, district_lgd_code={self.district_lgd_code})>"

    def json(self):
        return {
            "id": self.id,
            "state_lgd_code": self.state_lgd_code,
            "district_lgd_code": self.district_lgd_code,
            "lgd_code": self.lgd_code,
            "block_name": self.block_name
        }

    @classmethod
    def get_aspirational_blocks(cls, district_lgd_code):
        results = cls.query.filter(cls.lgd_code.in_([4876,6653,7130,539,172,3209,6050,7047,4027,3784,4010,3979,3837,4628,624,781,762,2157,6287,6468,6255,5250,951,823,994]), 
                                   cls.district_lgd_code==district_lgd_code).order_by(cls.block_name).all()
        if results:
            json_data = [result.json() for result in results]
            return json_data
        else:
            return None 
    @classmethod    
    def get_id_and_name(cls, block_id, district_id, state_id):
        # Perform ORM query
        query = (
            db.session.query(
                cls.id.label('block_id'),
                cls.block_name.label('block_name'),
                District.id.label('district_id'),
                District.district_name.label('district_name'),
                State.id.label('state_id'),
                State.state_name.label('state_name'),
            )
            .join(District, District.lgd_code == cls.district_lgd_code)
            .join(State, State.lgd_code == District.state_lgd_code)
            .filter(cls.id == block_id, District.id == district_id)
            .order_by(cls.block_name)
        )

        # Fetch the first result
        result = query.first()

        # Check if a result exists and format the response
        if result:
            json_data = {
                'block': {'id': result.block_id, 'name': result.block_name},
                'district': {'id': result.district_id, 'name': result.district_name},
                'state': {'id': result.state_id, 'name': result.state_name},
            }
            return json_data
        else:
            return None

    
    @classmethod
    def get_blocks(cls, district_id):
        results = cls.query.filter_by(district_id = district_id).order_by(cls.name).all()
        if results:
            json_data = [result.json() for result in results]
            return json_data
        else:
            return None
    
    @classmethod
    def get_district_by_block(cls, block_id):
        return cls.query.filter_by(id = block_id).first()