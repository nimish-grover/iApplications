from iJal.app.db import db

class BlockWaterTransfer(db.Model):
    __tablename__ = "block_water_transfers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    transfer_quantity = db.Column(db.Float, nullable=False)
    transfer_type_id = db.Column(db.ForeignKey('block_transfer_types.id'), nullable=False)
    transfer_sector_id = db.Column(db.ForeignKey('block_transfer_sectors.id'), nullable=False)

    transfer_type = db.relationship('BlockTransferType', backref = db.backref('block_water_transfers', lazy='dynamic'))
    transfer_sector = db.relationship('BlockTransferSector', backref = db.backref('block_water_transfers', lazy='dynamic'))

    def __init__(self, transfer_quantity, transfer_type_id, transfer_sector_id, column_4):
        self.transfer_quantity = transfer_quantity
        self.transfer_type_id = transfer_type_id
        self.transfer_sector_id = transfer_sector_id

    def json(self):
        return {
            'id': self.id,
            'transfer_quantity': self.transfer_quantity,
            'transfer_type_id': self.transfer_type_id,
            'transfer_sector_id': self.transfer_sector_id
        }