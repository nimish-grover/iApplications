from iJalagam.app import db


class Livestock(db.Model):
    __tablename__ = "livestocks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # Name of the livestock.e.g. cattle, buffalo
    category = db.Column(db.String(100), nullable=False) # Category viz. animal, bird
    coefficient = db.Column(db.Float, nullable=False, default=0) # water consumption calcultation coefficient
    remarks = db.Column(db.String(300)) # e.g. - description of item.

    def __init__(self, name, category, coefficient, remarks):
        self.name = name
        self.coefficient = coefficient
        self.category = category
        self.remarks = remarks

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'coefficient': self.coefficient,
            'category': self.category,
            'remarks': self.remarks
        }