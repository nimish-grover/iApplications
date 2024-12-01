from iJalagam.app import db


class Crop(db.Model):
    __tablename__ = "crops"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False )
    coefficient = db.Column(db.Float, nullable=False, default=0)
    remarks = db.Column(db.String(300),nullable=True )

    def __init__(self, name, coefficient, remarks):
        self.name = name
        self.coefficient = coefficient
        self.remarks = remarks

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'coefficient': self.coefficient,
            'remarks': self.remarks
        }

