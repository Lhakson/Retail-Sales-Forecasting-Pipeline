import logging
import pandas as pd
from prophet import Prophet
from src.db_manager import DBManager

def run_forecast():
    db = DBManager()
    
    # 1. Load the clean data
    with db.get_connection() as con:
        df = con.execute("SELECT date as ds, value as y FROM processed_sales").df()
    
    # 2. Configure Prophet with US Holidays
    model = Prophet(yearly_seasonality=True, interval_width=0.95)
    model.add_country_holidays(country_name='US')
    
    try:
        # 3. Train the model
        logging.info("Training Prophet model...")
        model.fit(df)
        
        # 4. Predict 12 months into the future
        future = model.make_future_dataframe(periods=24, freq='MS')
        forecast = model.predict(future)
        
        # 5. Save the forecast results
        with db.get_connection() as con:
            con.execute("CREATE OR REPLACE TABLE sales_forecast AS SELECT * FROM forecast")
            
        logging.info("Forecasting complete: 12-month prediction stored.")
        
    except Exception as e:
        logging.error(f"Forecasting failed: {e}")
        raise