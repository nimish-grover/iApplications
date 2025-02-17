from iLand.app.db import db

class District(db.Model):
    __tablename__ = 'districts'

    code = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(80),nullable=False)
    state_code = db.Column(db.Integer,nullable=False)


    def __init__(self,name,state_code):
        self.name=name
        self.state_code=state_code



    def json(self):
        return {
            'code': self.code,
            'name': self.name,
            'state_code' : self.state_code   
        }
    
    @classmethod
    def get_district_by_state_code(cls, _code):
        query=cls.query.filter_by(state_code=_code).order_by(cls.name).all()
        districts = []
        for item in query:
            districts.append(item.json())
        if districts:
            return districts
        else:
            return None
        
    @classmethod
    def get_district_by_code(cls, _code):
        query=cls.query.filter_by(code=_code).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_district_by_name(cls, _name):
        query =  cls.query.filter_by(username=_name).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.code)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_code):
        participant = District.query.filter_by(code=_code).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_code):
        user = District.query.filter_by(code=_code).update(data)
        db.session.commit()