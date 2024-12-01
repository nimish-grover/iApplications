
from iJalagam.app.db import db

class Village(db.Model):
    __tablename__ = 'villages'
    __table_args__ = (
        db.UniqueConstraint('block_id', 'district_id', 'id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    code = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50))
    status = db.Column(db.String(50))
    census_code = db.Column(db.Integer)
    local_name = db.Column(db.String(100))
    
    block_id = db.Column(db.ForeignKey('blocks.id'), nullable=False)
    district_id = db.Column(db.ForeignKey('districts.id'), nullable=False)
    state_id = db.Column(db.ForeignKey('states.id'), nullable=False)

    block = db.relationship('Block')
    district = db.relationship('District')
    state = db.relationship('State')

    def __init__(self, name, code, category, status, census_code, block_id, district_id, state_id, local_name):
        self.name = name
        self.code = code
        self.category = category
        self.status = status
        self.census_code = census_code
        self.block_id = block_id
        self.district_id = district_id
        self.state_id = state_id
        self.local_name = local_name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'category': self.category,
            'status': self.status,
            'census_code': self.census_code,
            'district_id': self.district_id,
            'block_id': self.block_id,
            'state_id': self.state_id,
            'local_name': self.local_name
        }


    @classmethod
    def get_villages(cls, block_id):
        return cls.query.filter_by(block_id = block_id).order_by(cls.name).all()
    
    @classmethod
    def get_district_by_village(cls, village_id):
        return cls.query.filter_by(id = village_id).first()