from iWater.app.db import db

class Nrega_Assets(db.Model):
    __tablename__ = 'nrega_assets'

    id = db.Column(db.Integer, primary_key= True)
    work_code = db.Column(db.String(),nullable=False)
    work_name=db.Column(db.String(),nullable=False)
    sanction_amount = db.Column(db.Integer(),nullable = False)
    total_amount = db.Column(db.Integer(),nullable = False)
    total_mandays = db.Column(db.Integer(),nullable = False)
    work_started_on = db.Column(db.String(20),nullable = False)
    work_completed_on = db.Column(db.String(20),nullable = False)
    financial_year = db.Column(db.String(20),nullable = False)
    
    
    panchayat_id = db.relationship('')
    work_category_id = db.relationship('')
    work_type_id = db.relationship('')
    
    def __init__(self,work_name,work_code,work_type_id,work_category_id,sanction_amount,total_amount,total_mandays,work_started_on,work_completed_on,financial_year,panchayat_id):
        self.work_name=work_name
        self.work_code = work_code
        self.work_type_id = work_type_id,
        self.work_category_id = work_category_id
        self.sanction_amount = sanction_amount
        self.total_amount =total_amount
        self.total_mandays = total_mandays
        self.work_started_on = work_started_on
        self.work_completed_on = work_completed_on
        self.financial_year = financial_year
        self.panchayat_id = panchayat_id


    
    def json(self):
        return {
            'id': self.id,
            'work_name' : self.work_name,
            'work_code': self.work_code,
            'work_type_id' : self.work_type_id ,
            'sanction_amount' : self.sanction_amount ,
            'total_amount' : self.total_amount ,
            'total_mandays' : self.total_mandays ,
            'work_started_on' : self.work_started_on ,
            'work_completed_on' :self.work_completed_on ,
            'financial_year' : self.financial_year ,
            'panchayat_id' : self.panchayat_id 
        }
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.description)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_id):
        participant = Nrega_Assets.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = Nrega_Assets.query.filter_by(id=_id).update(data)
        db.session.commit()