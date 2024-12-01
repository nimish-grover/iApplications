from iJalagam.app.db import db

class District(db.Model):
    __tablename__ = 'districts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.Integer, nullable=False, unique=True)
    census_code = db.Column(db.Integer)
    state_id = db.Column(db.ForeignKey('states.id'), nullable=False)
    local_name = db.Column(db.String(100))

    state = db.relationship('State')

    def __init__(self, name, code, census_code, state_id, local_name):
        self.name = name
        self.code = code
        self.census_code = census_code
        self.state_id = state_id
        self.local_name = local_name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'census_code': self.census_code,
            'state_id': self.state_id,
            'local_name': self.local_name
        }


    @classmethod
    def get_districts(cls, state_id):
        results = cls.query.filter_by(state_id = state_id).order_by(cls.name).all()
        if results:
            json_data = [result.json() for result in results]
            return json_data
        else:
            return None
    
    @classmethod
    def get_aspirational_districts(cls, state_id):
        results = cls.query.filter(cls.code.in_([745,196,641,72,20,338,563,9,434,398,431,426,405,500,92,115,112,227,583,596,610,721,129,119,132]), 
                                   cls.state_id==state_id).order_by(cls.name).all()
        if results:
            json_data = [result.json() for result in results]
            return json_data
        else:
            return None