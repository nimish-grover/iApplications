from iJal.app.db import db


class BlockTransferSector(db.Model):
    __tablename__ = "block_transfer_sectors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    sector = db.Column(db.String(100), unique=True, nullable=False)
    remarks = db.Column(db.String(200))

    def __init__(self, sector, remarks):
        self.sector = sector
        self.remarks = remarks

    def json(self):
        return {
            'id': self.id,
            'sector': self.sector,
            'remarks': self.remarks
        }