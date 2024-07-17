from iWater.app.db import db

class Livestock(db.Model):
    __tablename__ = 'livestocks'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('livestocks_id_seq'::regclass)"))
    type = db.Column(db.String(20))
    bird_type = db.Column(db.String(30))
    name = db.Column(db.String(80), nullable=False, unique=True)
    water_use = db.Column(db.Float(53), nullable=False)

    def json(self):
        return{
            'id': self.id,
            'type': self.type,
            'bird_type': self.bird_type,
            'name': self.name,
            'water_use': self.water_use
        }
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.id).all()
        arr =[]
        for row in query:
            row.json()
            arr.append(row)
        return arr
    
    @classmethod
    def get_by_type(cls, _type):
        query =  cls.query.filter_by(type=_type).all()
        if query:
            return query
        else:
            return None
        
    @classmethod
    def get_by_name(cls, _name):
        query=cls.query.filter_by(name=_name).first()
        if query:
            return query.json()
        else:
            return None