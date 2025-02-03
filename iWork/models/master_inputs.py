from iWater.app.db import db

class Inputs(db.Model):
    __tablename__ = 'master_inputs'

    id = db.Column(db.Integer, primary_key= True)
    input = db.Column(db.String(80),nullable=False)
    description=db.Column(db.String(),nullable=False)
    

    
    def __init__(self,description,input):
        self.description=description
        self.input = input
        


    
    def json(self):
        return {
            'id': self.id,
            'description' : self.description,
            'input': self.input
            
        }
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.description)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_id):
        participant = Inputs.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = Inputs.query.filter_by(id=_id).update(data)
        db.session.commit()