from sqlalchemy import case, func, text
from iJal.app.db import db
from zoneinfo import ZoneInfo
from datetime import datetime

from iJal.app.models.block_transfer_sector import BlockTransferSector
from iJal.app.models.block_transfer_type import BlockTransferType

class BlockWaterTransfer(db.Model):
    def get_current_time():
        return datetime.now(ZoneInfo('Asia/Kolkata'))
    
    __tablename__ = "block_water_transfers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    transfer_quantity = db.Column(db.Float, nullable=False)
    transfer_type_id = db.Column(db.ForeignKey('block_transfer_types.id'), nullable=False)
    transfer_sector_id = db.Column(db.ForeignKey('block_transfer_sectors.id'), nullable=False)
    bt_id = db.Column(db.ForeignKey('block_territory.id'), nullable=False)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    created_on = db.Column(db.DateTime, default=get_current_time)
    lulc_id = db.Column(db.ForeignKey('lulc.id'), nullable=False)
    created_by = db.Column(db.ForeignKey('users.id'), nullable=False)

    transfer_type = db.relationship('BlockTransferType', backref = db.backref('block_water_transfers', lazy='dynamic'))
    transfer_sector = db.relationship('BlockTransferSector', backref = db.backref('block_water_transfers', lazy='dynamic'))

    def __init__(self, transfer_quantity, transfer_type_id, transfer_sector_id,is_approved,created_by, bt_id):
        self.transfer_quantity = transfer_quantity
        self.transfer_type_id = transfer_type_id
        self.transfer_sector_id = transfer_sector_id
        self.bt_id = bt_id
        self.is_approved = is_approved
        self.created_by = created_by

    def json(self):
        return {
            'id': self.id,
            'transfer_quantity': self.transfer_quantity,
            'transfer_type_id': self.transfer_type_id,
            'transfer_sector_id': self.transfer_sector_id
        }
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.id==id).first()
    
    @classmethod
    def get_by_bt_id(cls, bt_id):
        query = db.session.query(
            BlockTransferType.id.label("type_id"),
            BlockTransferSector.id.label("sector_id"),
            func.concat(
                BlockTransferType.transfer_type, 
                ' (', 
                BlockTransferSector.sector, 
                ')'
            ).label("water_transfer"),
            func.coalesce(
                case(
                    (BlockWaterTransfer.bt_id == bt_id, BlockWaterTransfer.transfer_quantity),  # Positional arguments for `whens`
                    else_=0
                ),
                0
            ).label("transfer_quantity")
        ).select_from(BlockTransferType
        ).join(BlockTransferSector, text("1=1")
        ).outerjoin(
            BlockWaterTransfer,
            (BlockTransferType.id == BlockWaterTransfer.transfer_type_id) &
            (BlockTransferSector.id == BlockWaterTransfer.transfer_sector_id)
        ).order_by(BlockTransferType.id, BlockTransferSector.id)

        # Execute the query
        results = query.all()

        if results:
            json_data = [{
                'id': index + 1,
                'bt_id': bt_id,
                'type_id':item.type_id,
                'sector_id':item.sector_id,
                'water_transfer':item.water_transfer,
                'quantity':item.transfer_quantity,
            } for index,item in enumerate(results)]
            return json_data
        return None
    
    def update_db(self):
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def delete_from_db(cls,object):
        db.session.delete(object)
        db.session.commit()
