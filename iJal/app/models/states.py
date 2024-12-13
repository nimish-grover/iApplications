from iJal.app.db import db
from iJal.app.models.districts import District

class State(db.Model):
    __tablename__ = 'states'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    lgd_code = db.Column(db.Integer, unique=True, nullable=True)
    state_name = db.Column(db.String(255), nullable=True)
    census_code = db.Column(db.Integer, nullable=True)
    is_state = db.Column(db.Boolean, nullable=True, default=True)

    def __init__(self, lgd_code, state_name=None, census_code=None, is_state=None):
        self.lgd_code = lgd_code
        self.state_name = state_name
        self.census_code = census_code
        self.is_state = is_state

    def __repr__(self):
        return f"<State(id={self.id}, lgd_code={self.lgd_code}, state_name={self.state_name})>"

    def json(self):
        return {
            "id": self.id,
            "lgd_code": self.lgd_code,
            "state_name": self.state_name,
            "census_code": self.census_code,
            "is_state": self.is_state
        }
    
    @classmethod
    def get_states_by_id(cls, state_id):
        results = cls.query.filter_by(id=state_id).all()
        if results:
            json_data = [{'tj_id':0,'id':item.id,'name':item.state_name,'code':item.lgd_code} for item in results]
            return json_data
        else:
            return None


