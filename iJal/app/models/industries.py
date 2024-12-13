from iJal.app.db import db


class Industry(db.Model):

    __tablename__ = 'industries'

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    industry_sector = db.Column(db.String(200), nullable=False, unique=True)

    def __init__(self, industry_sector):
        self.industry_sector = industry_sector

    def json(self):
        return {
            'id': self.id,
            'industry_sector' : self.industry_sector
        }
    
    @classmethod
    def get_all_industries(cls):
        return cls.query.all()
