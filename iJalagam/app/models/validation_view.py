from iJalagam.app.db import db
from sqlalchemy import text

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

    # Function to create the materialized view
    def create_validation_view():
        view_query = text("""
        CREATE MATERIALIZED VIEW validation_view AS
        SELECT 
            s.state_name,
            s.id AS state_id,
            s.short_name AS state_short_name,
            d.district_name,
            d.id AS district_id,
            b.block_name,
            b.id AS block_id,
            COALESCE(bt.id, 0) AS bt_id,
            COALESCE(MAX(CASE WHEN bp.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS population,
            COALESCE(MAX(CASE WHEN bl.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS livestock,
            COALESCE(MAX(CASE WHEN bc.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS crop,
            COALESCE(MAX(CASE WHEN bi.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS industry,
            COALESCE(MAX(CASE WHEN bwb.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS surface,
            COALESCE(MAX(CASE WHEN bg.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS ground,
            COALESCE(MAX(CASE WHEN blulc.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS lulc,
            COALESCE(MAX(CASE WHEN br.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS rainfall,
            COALESCE(MAX(CASE WHEN bwt.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS water_transfer
        FROM 
            states s
        LEFT JOIN districts d ON d.state_lgd_code = s.lgd_code
        LEFT JOIN blocks b ON b.district_lgd_code = d.lgd_code
        LEFT JOIN block_territory bt ON bt.block_id = b.id
        LEFT JOIN block_pops bp ON bp.bt_id = bt.id
        LEFT JOIN block_crops bc ON bc.bt_id = bt.id
        LEFT JOIN block_livestocks bl ON bl.bt_id = bt.id
        LEFT JOIN block_industries bi ON bi.bt_id = bt.id
        LEFT JOIN block_waterbodies bwb ON bwb.bt_id = bt.id
        LEFT JOIN block_groundwater bg ON bg.bt_id = bt.id
        LEFT JOIN block_lulc blulc ON blulc.bt_id = bt.id
        LEFT JOIN block_rainfall br ON br.bt_id = bt.id
        LEFT JOIN block_water_transfers bwt ON bwt.bt_id = bt.id
        WHERE 
            b.lgd_code IN (4876, 1740, 7130, 539, 172, 3209, 6050, 7047, 3784, 3837, 3979, 4010, 4027, 4628, 624, 762, 781, 2157, 6255, 6287, 6468, 5250, 823, 951, 994)
            AND d.lgd_code IN (745, 196, 641, 72, 20, 338, 563, 9, 434, 398, 431, 426, 405, 500, 92, 115, 112, 227, 583, 596, 610, 721, 129, 119, 132)
        GROUP BY 
            s.state_name,
            d.district_name,
            b.block_name,
            bt.id,
            s.id,
            d.id,
            b.id,
            s.short_name
        ORDER BY 
            s.state_name;
        """)
        
        db.session.execute(view_query)
        db.session.commit()

    # Function to refresh the materialized view
    def refresh_validation_view():
        refresh_query = text("REFRESH MATERIALIZED VIEW validation_view;")
        db.session.execute(refresh_query)
        db.session.commit()