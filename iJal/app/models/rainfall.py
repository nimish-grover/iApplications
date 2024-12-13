# from datetime import datetime
from sqlalchemy import Numeric, alias, and_, cast, func
from iJal.app.db import db

class Rainfall(db.Model):
    __tablename__ = 'rainfall_data'

    id = db.Column(db.Integer, primary_key=True)
    observation_date = db.Column(db.DateTime)
    normal = db.Column(db.Float(53), nullable=False)
    actual = db.Column(db.Float(53), nullable=False)
    district_id = db.Column(db.ForeignKey('districts.id'), nullable=False)
    
    district = db.relationship('District', backref=db.backref("rainfall_data", lazy="dynamic"))

    def __init__(self, observation_date, normal, actual, district_id):
        self.observation_date = observation_date
        self.normal = normal
        self.actual = actual
        self.district_id = district_id

    def json(self):
        return {
            'id': self.id,
            'observation_date': self.observation_date,
            'normal': self.normal,
            'actual': self.actual,
            'district_id': self.district_id 
        }
 
    @classmethod
    def get_monthwise_rainfall(cls, district_id):
        query = (
            db.session.query(
                func.to_char(cls.observation_date, 'FMMon-YY').label('month_year'),     # TO_CHAR
                func.round(cast(func.sum(cls.actual), Numeric), 2).label('actual'),      # SUM and ROUND
                func.round(cast(func.sum(cls.normal), Numeric), 2).label('normal')       # SUM and ROUND
            ).filter(cls.district_id==district_id)                                       # WHERE 
            .group_by(func.to_char(cls.observation_date, 'FMMon-YY'))                   # GROUP BY
            .order_by(func.min(cls.observation_date))                                    # ORDER BY
        )
        results = query.all()
        if results:
            result = [{'month':result[0],'actual':result[1],'normal':result[2]} for result in results]
        else: 
            result = [{'month':0,'actual':0,'normal':0}]
        return result
        # '''
        # SELECT
        # TO_CHAR(observation_date, 'Mon-YYYY') AS observation,
        # SUM(actual) AS actual
        # FROM
        #     rainfall_data
        # WHERE
        #     EXTRACT(YEAR FROM observation_date) = 2023 and district_id = 639
        # GROUP BY
        #     observation, EXTRACT(MONTH FROM observation_date), EXTRACT(YEAR FROM observation_date)
        # ORDER BY
        #     EXTRACT(YEAR FROM observation_date), EXTRACT(MONTH FROM observation_date);
        # '''
       