from iJalagam.app.db import db
from iJalagam.app.models.districts import District

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
    def get_aspirational_states(cls):
        results = cls.query.join(District, District.state_lgd_code==cls.lgd_code
                                ).filter(District.lgd_code.in_([745,196,641,72,20,338,563,9,434,398,431,426,405,500,92,115,112,227,583,596,610,721,129,119,132])
                                ).order_by(cls.state_name).all()
        if results:
            return [result.json() for result in results]
        else:
            return None

    @classmethod
    def get_lgd_code(cls,state_id):
        query = db.session.query(cls.lgd_code).filter_by(id=state_id).scalar()
        if query:
            return query
        else:
            return None
