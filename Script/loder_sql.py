import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

class DataLoader_SQL:
    def __init__(self):
        self.file_path = "DATA/cleaned_master_sales.csv"

    def load_data(self):
        try:
            # Load cleaned data
            DB_USER = os.getenv("DB_USER")
            DB_USER = os.getenv("DB_USER")
            DB_PASSWORD = os.getenv("DB_PASSWORD")
            DB_HOST = os.getenv("DB_HOST")
            DB_PORT = os.getenv("DB_PORT")
            DB_NAME = os.getenv("DB_NAME")

            engine = create_engine(
                f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
            df = pd.read_csv(self.file_path)
            df.to_sql("master_sales", engine, if_exists="replace", index=False)



            print("Data successfully loaded into MySQL!✅")
        except Exception as e:
            print(f"Error loading data: {e}")
            return None