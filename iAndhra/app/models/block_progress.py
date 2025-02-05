from sqlalchemy import Integer, cast, func
from iAndhra.app.db import db
from datetime import datetime
from zoneinfo import ZoneInfo
from iAndhra.app.models.states import State
from iAndhra.app.models.districts import District
from iAndhra.app.models.blocks import Block
from iAndhra.app.models.block_territory import BlockTerritory
from iAndhra.app.models.block_category import BlockCategory

class BlockProgress(db.Model):
    def get_current_time():
        return datetime.now(ZoneInfo('Asia/Kolkata'))
    __tablename__ = 'block_progress'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    bt_id = db.Column(db.Integer, db.ForeignKey('block_territory.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('block_category.id'), nullable=False)
    table_id = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    created_on = db.Column(db.DateTime, default=get_current_time)

    # Relationships (if needed)
    block_territory = db.relationship('BlockTerritory', backref=db.backref('block_progress', lazy='dynamic'))
    block_category = db.relationship('BlockCategory', backref=db.backref('block_progress', lazy='dynamic'))
    
    def __init__(self, bt_id, is_approved, category_id, value,table_id):

        self.bt_id = bt_id
        self.is_approved = is_approved
        self.category_id = category_id
        self.value = value
        self.table_id = table_id
        
    def json(self):
        """
        Returns a JSON serializable dictionary representation of the Village instance.
        """
        return {
            "id": self.id,
            "bt_id": self.bt_id,
            "is_approved": self.is_approved,
            "created_on": self.created_on,
            "category_id": self.category_id,
            "value": self.value,
            "table_id": self.table_id
        }
        
    @classmethod
    def check_duplicate(cls, category_id,table_id, bt_id):
        return cls.query.filter(cls.table_id==table_id,cls.category_id==category_id,cls.bt_id==bt_id).first()
    
    @classmethod
    def get_progress_check(cls,bt_id,category_id):
        query = db.session.query(cls.id).filter(cls.bt_id == bt_id, cls.category_id==category_id).all()
        if query:
            return True
    
    def transform_data(data):
        output = []
        colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4']
        color_index = 0

        for block in data:
            block_id = block['block_id']
            block_data = block['data']

            # Calculate percentage/completed (assume 100% completion if all `is_approved` are 1)
            completed = sum(1 for entry in block_data if entry['is_approved'] == 1)
            percentage = completed * 100 // len(block_data)

            # Take the first entry as representative for static fields
            first_entry = block_data[0]
            temp_dict={}
            temp_dict['state_name']=first_entry['state_name']
            temp_dict['state_short_name']=first_entry['state_short_name']
            temp_dict['state_id'] = first_entry['state_id']
            temp_dict['block_id'] = first_entry['block_id']
            temp_dict['district_id'] = first_entry['district_id']
            temp_dict['district_name']=first_entry['district_name']
            temp_dict['block_name']= first_entry['block_name']
            temp_dict['completed']= percentage
            temp_dict['percentage'] = percentage
            temp_dict['color']= colors[color_index % len(colors)]
            for block in block_data:
                category_id = block['category_id']
                if category_id:
                    category=BlockCategory.get_category_name(category_id)
                    temp_dict[category] = block['is_approved']
            output.append(temp_dict)
            color_index += 1
            
        sorted_dict = sorted(output, key=lambda x: x["completed"])
        for idx, item in enumerate(sorted_dict):
            item['id'] = idx + 1
        return sorted_dict

    @classmethod
    def get_all_states_status(cls):
        block_lgd_codes = [4876, 1740, 7130, 539, 172, 3209, 6050, 7047, 3784, 3837, 3979, 4010, 4027, 4628, 624, 762, 781, 2157, 6255, 6287, 6468, 5250, 823, 951, 994]
        district_lgd_codes = [745, 196, 641, 72, 20, 338, 563, 9, 434, 398, 431, 426, 405, 500, 92, 115, 112, 227, 583, 596, 610, 721, 129, 119, 132]
        query = (db.session.query(
                State.state_name.label("state_name"),
                State.short_name.label("state_short_name"),
                State.id.label("state_id"),
                District.district_name.label("district_name"),
                District.id.label("district_id"),
                Block.block_name.label("block_name"),
                Block.id.label("block_id"),
                func.coalesce(BlockProgress.category_id, 0).label("category_id"),
                func.coalesce(BlockProgress.bt_id, 0).label("bt_id"),
                func.coalesce(func.min(cast(BlockProgress.is_approved, Integer)), 0).label("is_approved"),
            )
            .join(District, District.lgd_code == Block.district_lgd_code, isouter=True)
            .join(State, State.lgd_code == District.state_lgd_code, isouter=True)
            .join(BlockTerritory, BlockTerritory.block_id == Block.id, isouter=True)
            .join(BlockProgress, BlockProgress.bt_id == BlockTerritory.id, isouter=True)
            .filter(Block.lgd_code.in_(block_lgd_codes))
            .filter(District.lgd_code.in_(district_lgd_codes))
            .group_by(
                BlockProgress.category_id,
                State.state_name,
                State.id,
                State.short_name,
                District.district_name,
                District.id,
                Block.block_name,
                Block.id,
                BlockProgress.bt_id
            )
            .order_by(BlockProgress.bt_id, BlockProgress.category_id)
        )
        
        results = query.all()
        grouped_data = {}
        for row in results:
            block_id = str(row[6])  # Convert block_id to string for consistency
            # Create a dictionary for each row
            row_dict = {
                "state_name": row[0],
                "state_short_name": row[1],
                "state_id": row[2],
                "district_name": row[3],
                "district_id": row[4],
                "block_name": row[5],
                "block_id": row[6],
                "category_id": row[7],
                "bt_id": row[8],
                "is_approved": row[9],
            }
            # Check if the block_id already exists in grouped_data
            if block_id not in grouped_data:
                grouped_data[str(block_id)] = []  # Initialize with an empty list
            grouped_data[str(block_id)].append(row_dict)  # Append the row to the group

        # Convert grouped data to the desired format
        result = [{"block_id": block_id, "data": rows} for block_id, rows in grouped_data.items()]
        
        return BlockProgress.transform_data(result)


    
    def save_to_db(self):
        duplicate_item = self.check_duplicate(self.category_id,self.table_id,self.bt_id)
        if duplicate_item:
            duplicate_item.value = self.value
            duplicate_item.created_on = BlockProgress.get_current_time()
            duplicate_item.is_approved = self.is_approved
            duplicate_item.update_db()
        else:
            db.session.add(self)
        db.session.commit()
        
    def update_db(self):
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()