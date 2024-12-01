from iJalagam.app import db

class WaterbodyType(db.Model):
    __tablename__ = "waterbody_types"

    id = db.Column(db.Integer, primary_key=True)
    waterbody_type = db.Column(db.String(80), nullable=False)

    def __init__(self, waterbody_type):
        self.waterbody_type = waterbody_type

    def json(self):
        return {
            'waterbody_type': self.waterbody_type
        }