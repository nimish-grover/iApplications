from iJalagam.app.db import db
import asyncio
from sqlalchemy import text

# import asyncpg
class ValidationView(db.Model):
    __tablename__ = 'validation_view'
    
    # Primary key will be composite of state_id, district_id, block_id, bt_id
    state_id = db.Column(db.Integer, primary_key=True)
    district_id = db.Column(db.Integer, primary_key=True)
    block_id = db.Column(db.Integer, primary_key=True)
    bt_id = db.Column(db.Integer, primary_key=True)
    
    # Other columns
    state_name = db.Column(db.String)
    state_short_name = db.Column(db.String)
    district_name = db.Column(db.String)
    block_name = db.Column(db.String)
    population = db.Column(db.Integer)
    livestock = db.Column(db.Integer)
    crop = db.Column(db.Integer)
    industry = db.Column(db.Integer)
    surface = db.Column(db.Integer)
    ground = db.Column(db.Integer)
    lulc = db.Column(db.Integer)
    rainfall = db.Column(db.Integer)
    water_transfer = db.Column(db.Integer)
    updated_time = db.Column(db.DateTime)


    
    @classmethod 
    def get_validation_view_data(cls):
        query = cls.query.order_by(
            cls.state_name,
            cls.district_name,
            cls.block_name
        )
        
        results = query.all()
        results_dict = []
        
        for row in results:
            row_dict = {
                'state_name': row.state_name,
                'state_short_name': row.state_short_name,
                'district_name': row.district_name,
                'block_name': row.block_name,
                'population': row.population,
                'livestock': row.livestock,
                'crop': row.crop,
                'industry': row.industry,
                'surface': row.surface,
                'ground': row.ground,
                'lulc': row.lulc,
                'rainfall': row.rainfall,
                'water_transfer': row.water_transfer,
                'updated_time': row.updated_time
            }
            
            status_count = 0 
            category = ['population','livestock','crop','industry','surface','ground','lulc','rainfall','water_transfer']
            for item in category:
                if row_dict[item]:
                    status_count += 1
            if status_count < 9 and status_count > 0:
                row_dict['completed'] = 11 * status_count
            elif status_count == 9:
                row_dict['completed'] = 100
            else:
                row_dict['completed'] = 0 
                
            dt_object = row_dict['updated_time']
            row_dict['updated_time'] = dt_object.strftime("%d-%m-%y, %H:%M:%S")
            results_dict.append(row_dict)
        
        sorted_dict = sorted(results_dict, key=lambda x: x["completed"])
        for idx, item in enumerate(sorted_dict):
            item['id'] = idx + 1
        
        return sorted_dict

    @classmethod
    async def refresh_validation_view_async(cls):
        """Async method to refresh the materialized view."""
        try:
            # Just the command to refresh the materialized view asynchronously
            # Your existing logic to run refresh operation (no database connection here)
            sql = text("REFRESH MATERIALIZED VIEW CONCURRENTLY validation_view")
            result = db.session.execute(sql)

            print("Materialized view refresh triggered.")  # Placeholder for the actual refresh command
        except Exception as e:
            print(f"Error refreshing materialized view: {e}")

    @classmethod
    def refresh_validation_view(cls):
        """Method to run the refresh asynchronously in a separate thread."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(cls.refresh_validation_view_async())
