import pandas as pd
from exception import CustomException
from logger import logging
import sys
from matrix import Matrix,MatrixConfig

logging.info("ETL Process Started")
print("ETL Process Started")

class ETLconfig:
    def __init__(self, amazon_path: str, international_path: str, master_sales_path: str, cleaned_data_path: str):
        self.amazon_path = amazon_path
        self.international_path = international_path
        self.master_sales_path = master_sales_path
        self.cleaned_data_path = cleaned_data_path


class ETL:
    def __init__(self):
        logging.info("ETL Config Initialized with paths: Amazon - {0}, International - {1}".format(
            "DATA/Amazon Sale Report.csv",
            "DATA/International Sale Report.csv"
        ))
        self.config = ETLconfig(
            amazon_path="DATA/Amazon Sale Report.csv",
            international_path="DATA/International Sale Report.csv",
            master_sales_path="DATA/master_sales.csv",
            cleaned_data_path="DATA/cleaned_master_sales.csv"
        )

    def margedata(self):
        try:
            # Load files
            logging.info("Loading data from paths: Amazon - {0}, International - {1}".format(
                self.config.amazon_path,
                self.config.international_path
            ))
            amazon = pd.read_csv(self.config.amazon_path, low_memory=False)
            international = pd.read_csv(self.config.international_path)

            # Strip column spaces
            logging.info("Stripping column spaces for both datasets")
            amazon.columns = amazon.columns.str.strip()
            international.columns = international.columns.str.strip()

            # ---------------- AMAZON ----------------
            logging.info("Renaming columns for Amazon dataset")
            amazon = amazon.rename(columns={
                "Date": "order_date",
                "SKU": "sku",
                "Qty": "quantity",
                "Amount": "revenue",
                "ship-country": "country"
            })

            amazon["source"] = "Amazon"

            amazon = amazon[["order_date", "sku", "quantity", "revenue", "country", "source"]]

            # ---------------- INTERNATIONAL ----------------
            logging.info("Renaming columns for International dataset")
            international = international.rename(columns={
                "DATE": "order_date",
                "SKU": "sku",
                "PCS": "quantity",
                "GROSS AMT": "revenue"
            })

            international["country"] = "International"
            international["source"] = "International"

            international = international[["order_date", "sku", "quantity", "revenue", "country", "source"]]

            # ---------------- Cleaning ----------------
            logging.info("Cleaning data: Converting data types and standardizing SKU format")
            amazon["order_date"] = pd.to_datetime(amazon["order_date"], errors="coerce")
            international["order_date"] = pd.to_datetime(international["order_date"], errors="coerce")

            amazon["revenue"] = pd.to_numeric(amazon["revenue"], errors="coerce")
            international["revenue"] = pd.to_numeric(international["revenue"], errors="coerce")

            amazon["quantity"] = pd.to_numeric(amazon["quantity"], errors="coerce")
            international["quantity"] = pd.to_numeric(international["quantity"], errors="coerce")

            amazon["sku"] = amazon["sku"].astype(str).str.upper().str.replace(" ", "")
            international["sku"] = international["sku"].astype(str).str.upper().str.replace(" ", "")

            # ---------------- APPEND ----------------
            logging.info("Appending datasets to create master_sales")
            master_sales = pd.concat([amazon, international], ignore_index=True)

            # Remove duplicates
            logging.info("Removing duplicates from master_sales")
            master_sales = master_sales.drop_duplicates()

            # Save
            logging.info("Saving master_sales to path: {0}".format(self.config.master_sales_path))
            master_sales.to_csv(self.config.master_sales_path, index=False)

            print("FINAL SHAPE:", master_sales.shape)
            print(master_sales.head())
            
            

        except Exception as e:
            raise CustomException(e, sys)
        
    def clean_master_sales(self):
        try:
            logging.info("Loading master_sales from path: {0}".format(self.config.master_sales_path))
            master_sales = pd.read_csv(self.config.master_sales_path)
            
            logging.info("Cleaning master_sales: Handling missing values and extracting date components")
                
            print(master_sales.info())
            master_sales['quantity'] = master_sales['quantity'].astype(float)
            master_sales['revenue'] = master_sales['revenue'].astype(float)
            
            print(master_sales.isnull().sum())
                
            master_sales['order_date'] = master_sales['order_date'].fillna(master_sales['order_date'].mode()[0])
            master_sales['quantity'] = master_sales['quantity'].fillna(master_sales['quantity'].mode()[0])
            master_sales['revenue'] = master_sales['revenue'].fillna(master_sales['revenue'].mean())
                
            logging.info("Extracting year, month, and day from order_date")
                
            master_sales['order_date'] = master_sales['order_date'].astype(str)
            
                
            master_sales['year'] = master_sales['order_date'].str.split('-').str[0]
            master_sales['month'] = master_sales['order_date'].str.split('-').str[1]
            master_sales['day'] = master_sales['order_date'].str.split('-').str[2]
            
            master_sales = master_sales[
            (master_sales["revenue"] > 0) &
            (master_sales["quantity"] > 0) &
            (master_sales["sku"].notnull())
            ]

            
            logging.info("Saving cleaned master_sales to path: {0}".format(self.config.cleaned_data_path))
            master_sales.to_csv(self.config.cleaned_data_path, index=False)
                

        except Exception as e:
                raise CustomException(e, sys)


if __name__ == "__main__":
    try:
        etl_process = ETL()
        etl_process.margedata()
        etl_process.clean_master_sales()
        logging.info("ETL Process Completed Successfully")
        print("ETL Process Completed Successfully")
        matrix = Matrix()
        matrix.generate_correlation_matrix()
    except Exception as e:
        logging.error("ETL Process Failed with error: {0}".format(str(e)))
        print("ETL Process Failed with error:", str(e))