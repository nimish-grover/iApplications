-- create validation view 
CREATE MATERIALIZED VIEW mv_block_data AS
WITH filtered_data AS (
    SELECT 
        s.id AS state_id,
        s.state_name,
        s.short_name AS state_short_name,
        d.id AS district_id,
        d.district_name,
        b.id AS block_id,
        b.block_name
    FROM 
        states s
    JOIN districts d ON d.state_lgd_code = s.lgd_code
    JOIN blocks b ON b.district_lgd_code = d.lgd_code
    WHERE 
        b.lgd_code IN (4876, 1740, 7130, 539, 172, 3209, 6050, 7047, 3784, 3837, 3979, 4010, 4027, 4628, 624, 762, 781, 2157, 6255, 6287, 6468, 5250, 823, 951, 994)
        AND d.lgd_code IN (745, 196, 641, 72, 20, 338, 563, 9, 434, 398, 431, 426, 405, 500, 92, 115, 112, 227, 583, 596, 610, 721, 129, 119, 132)
)
SELECT 
    fd.state_name,
    fd.state_id,
    fd.state_short_name,
    fd.district_name,
    fd.district_id,
    fd.block_name,
    fd.block_id,
    COALESCE(bt.id, 0) AS bt_id,
    COALESCE(MAX(CASE WHEN bp.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS population,
    COALESCE(MAX(CASE WHEN bl.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS livestock,
    COALESCE(MAX(CASE WHEN bc.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS crop,
    COALESCE(MAX(CASE WHEN bi.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS industry,
    COALESCE(MAX(CASE WHEN bwb.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS surface,
    COALESCE(MAX(CASE WHEN bg.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS ground,
    COALESCE(MAX(CASE WHEN blulc.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS lulc,
    COALESCE(MAX(CASE WHEN br.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS rainfall,
    COALESCE(MAX(CASE WHEN bwt.is_approved = 'True' THEN 1 ELSE 0 END), 0) AS water_transfer,
    now() AT TIME ZONE 'Asia/Kolkata' AS updated_time
FROM 
    filtered_data fd
LEFT JOIN block_territory bt ON bt.block_id = fd.block_id
LEFT JOIN block_pops bp ON bp.bt_id = bt.id
LEFT JOIN block_crops bc ON bc.bt_id = bt.id
LEFT JOIN block_livestocks bl ON bl.bt_id = bt.id
LEFT JOIN block_industries bi ON bi.bt_id = bt.id
LEFT JOIN block_waterbodies bwb ON bwb.bt_id = bt.id
LEFT JOIN block_groundwater bg ON bg.bt_id = bt.id
LEFT JOIN block_lulc blulc ON blulc.bt_id = bt.id
LEFT JOIN block_rainfall br ON br.bt_id = bt.id
LEFT JOIN block_water_transfers bwt ON bwt.bt_id = bt.id
GROUP BY 
    fd.state_name,
    fd.state_id,
    fd.state_short_name,
    fd.district_name,
    fd.district_id,
    fd.block_name,
    fd.block_id,
    bt.id;



-- refresh validation_view 
CREATE OR REPLACE FUNCTION refresh_validation_view()
RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY validation_view;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


--asign triggers 
DO $$
DECLARE
    tbl_name TEXT;
BEGIN
    FOR tbl_name IN 
        SELECT unnest(ARRAY[
            'states', 'districts', 'blocks', 'block_territory', 
            'block_pops', 'block_crops', 'block_livestocks', 
            'block_industries', 'block_waterbodies', 'block_groundwater', 
            'block_lulc', 'block_rainfall', 'block_water_transfers'
        ])
    LOOP
        EXECUTE format(
            'CREATE TRIGGER trg_refresh_validation_view_%I
             AFTER INSERT OR UPDATE OR DELETE
             ON %I
             FOR EACH STATEMENT
             EXECUTE FUNCTION refresh_validation_view();',
            tbl_name, tbl_name
        );
    END LOOP;
END;
$$;

--verify triggers 
SELECT tgname, tgrelid::regclass AS table_name
FROM pg_trigger
WHERE tgname LIKE 'trg_refresh_validation_view%';



--create indexes 
CREATE UNIQUE INDEX validation_view_unique_idx
ON validation_view (state_id, district_id, block_id);
