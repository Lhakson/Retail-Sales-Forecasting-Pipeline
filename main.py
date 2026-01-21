import logging
import os
from dotenv import load_dotenv
from src.db_manager import DBManager
from src.ingest import fetch_live_data
from src.transform import transform_data
from src.forecast import run_forecast

# 1. Setup Logging - This creates a 'logs' folder and a record of every run
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("logs/pipeline.log"), # Saves to a file
        logging.StreamHandler()                # Prints to your terminal
    ]
)

def run_pipeline():
    # Load your API Key from .env
    load_dotenv()
    
    logging.info("--- Starting Retail Forecasting Pipeline ---")
    
    try:
        # Initialize Database Manager
        db = DBManager()
        db.initialize_schema()
        
        # Step 1: Ingest
        fetch_live_data()
        
        # Step 2: Transform
        transform_data()
        
        # Step 3: Forecast
        run_forecast()
        
        logging.info("--- Pipeline Completed Successfully! ---")
        print("\n✅ Success! Data is ready for the dashboard.")
        
    except Exception as e:
        logging.error(f"Pipeline crashed at some point: {e}")
        print(f"\n❌ Error: {e}. Check logs/pipeline.log for details.")

if __name__ == "__main__":
    run_pipeline()

    