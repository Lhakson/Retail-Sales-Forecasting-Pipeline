import logging
from src.db_manager import DBManager

def transform_data():
    db = DBManager()
    
    # We calculate growth using SQL Window Functions
    # NULLIF prevents 'Division by Zero' errors if data is missing
    query = """
    CREATE OR REPLACE TABLE processed_sales AS
    WITH base_data AS (
        SELECT 
            date, 
            value,
            LAG(value, 12) OVER (ORDER BY date) as last_year_value
        FROM raw_sales
    )
    SELECT 
        date,
        value,
        CASE 
            WHEN last_year_value IS NOT NULL AND last_year_value != 0 
            THEN ((value - last_year_value) / last_year_value) * 100 
            ELSE 0 
        END as yoy_growth_pct
    FROM base_data;
    """
    
    try:
        with db.get_connection() as con:
            con.execute(query)
        logging.info("Transformation successful: YoY growth calculated.")
    except Exception as e:
        logging.error(f"Transformation failed: {e}")
        raise

    