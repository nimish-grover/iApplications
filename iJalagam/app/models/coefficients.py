from iJalagam.app import db


class Coefficient(db.Model):
    __tablename__ = "coefficients"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable=False)
    entity = db.Column(db.String(80), nullable=False)
    coefficient = db.Column(db.Float, nullable = False )
    coefficient_unit = db.Column(db.String(20))

    def __init__(self, name, entity, coefficient, coefficient_unit):
        self.name = name
        self.entity = entity
        self.coefficient = coefficient
        self.coefficient_unit = coefficient_unit

    def json(self):
        return {
            'name': self.name,
            'entity': self.entity,
            'coefficient': self.coefficient,
            'coefficient_unit': self.coefficient_unit
        }
    
    @classmethod
    def get_livestock_coefficents(cls):
        results = cls.query.filter_by(entity='Livestock').all()
        json_data = [result.json() for result in results]
        json_data = [item for item in json_data if item['name']!='Camel']
        return json_data
    
    @classmethod
    def get_crop_coefficient(cls):
        results = cls.query.filter_by(entity='Crops').all()
        json_data = [result.json() for result in results]
        return json_data