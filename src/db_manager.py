import duckdb
import logging

class DBManager:
    def __init__(self, db_path='data/retail_warehouse.db'):
        self.db_path = db_path

    def get_connection(self):
        return duckdb.connect(self.db_path)

    def initialize_schema(self):
        with self.get_connection() as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS raw_sales (
                    date DATE PRIMARY KEY, 
                    value DOUBLE
                );
            """)
            logging.info("Schema verified.")