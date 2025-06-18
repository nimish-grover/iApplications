from datetime import datetime

import pytz
from iSaksham.app.db import db


class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(tz=pytz.timezone('Asia/Kolkata')), nullable=False)
    
    def __repr__(self):
        return f'<Activity: {self.action}>'