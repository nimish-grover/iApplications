from iWater.app.db import db

class Proposed_status(db.Model):
    __tablename__ = 'proposed_status'

    id = db.Column(db.Integer, primary_key= True)
    proposed_status=db.Column(db.String(80),nullable=False)
    work_type_id = db.Column(db.Integer,nullable = False)
    beneficiary_type_id = db.Column(db.Integer,nullable = False)
    activity_type_id = db.Column(db.Integer,nullable = False)
    major_head_id = db.Column(db.Integer,nullable = False)
    
    def __init__(self,proposed_status,work_type_id,beneficiary_type_id,activity_type_id,major_head_id,):
        self.proposed_status=proposed_status
        self.work_type_id = work_type_id
        self.beneficiary_type_id = beneficiary_type_id
        self.activity_type_id = activity_type_id
        self.major_head_id = major_head_id
    
    def json(self):
        return {
            'id': self.id,
            'proposed_status' : self.proposed_status,
            'work_type_id': self.work_type_id,
            'beneficiary_type_id' : self.beneficiary_type_id,
            'activity_type_id' : self.activity_type_id,
            'major_head_id' : self.major_head_id
        }
    
    @classmethod
    def get_wb_by_id(cls, _id):
        query=cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_wb_by_type_id(cls, _type_id):
        query =  cls.query.filter_by(type_id=_type_id).first()
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

    def delete_from_db(_id):
        participant = Proposed_status.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = Proposed_status.query.filter_by(id=_id).update(data)
        db.session.commit()