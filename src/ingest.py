import os
import requests
import pandas as pd
import logging
from src.db_manager import DBManager

def fetch_live_data():
    api_key = os.getenv("ALPHA_VANTAGE_KEY")
    if not api_key:
        raise ValueError("ALPHA_VANTAGE_KEY not found in .env file!")

    url = f'https://www.alphavantage.co/query?function=RETAIL_SALES&apikey={api_key}'
    
    try:
        logging.info("Fetching data from API...")
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
        
        if "data" not in data:
            logging.error(f"API Error: {data}")
            return

        df = pd.DataFrame(data['data'])
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'])
        
        db = DBManager()
        with db.get_connection() as con:
            con.register('df_view', df)
            # This logic prevents the 'Data Graveyard' (no duplicates!)
            con.execute("""
                INSERT INTO raw_sales 
                SELECT date, value FROM df_view
                ON CONFLICT (date) DO UPDATE SET value = excluded.value;
            """)
        logging.info(f"Ingested {len(df)} rows successfully.")
    except Exception as e:
        logging.error(f"Ingestion failed: {e}")
        raise