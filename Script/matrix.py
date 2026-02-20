import pandas as pd
from exception import CustomException
from logger import logging
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import os

logging.info("Matrix Script Started")
print("Matrix Script Started")


class MatrixConfig:
    def __init__(self, cleaned_data_path: str, matrix_output_path: str):
        self.cleaned_data_path = cleaned_data_path
        self.matrix_output_path = matrix_output_path
        
        
class Matrix:
    def __init__(self):
        logging.info("Matrix Config Initialized with paths: Cleaned Data - {0}, Matrix Output - {1}".format(
            "DATA/cleaned_master_sales.csv",
            "DATA/correlation_matrix.png"
        ))
        self.config = MatrixConfig(
            cleaned_data_path="DATA/cleaned_master_sales.csv",
            matrix_output_path="DATA/correlation_matrix.png"
        )

    def generate_correlation_matrix(self):
        try:
            os.makedirs("KPI", exist_ok=True)
            
            logging.info("Loading cleaned data from path: {0}".format(self.config.cleaned_data_path))
            df = pd.read_csv(self.config.cleaned_data_path)

            logging.info("Generating correlation matrix")
            total_revenue = int(df['revenue'].sum())
            print(f"total revenue: {total_revenue}")

            total_order = df['order_date'].nunique()
            print(f"total order: {total_order}")

            total_quantity_sold = int(df['quantity'].sum())
            print(f"total quantity sold: {total_quantity_sold}")

            Average_Order_Value = int(total_revenue / total_order if total_order > 0 else 0)
            print(f"Average Order Value: {Average_Order_Value}")

            revenue_by_source = df.groupby('source')['revenue'].sum()
            print("Revenue by Source:")
            print(revenue_by_source)
            revenue_by_source.plot(kind='bar', title='Revenue by Source')
            logging.info("Saving revenue by source plot to KPI/Revenue_Metrics/revenue_by_source.png")
            os.makedirs("KPI/Revenue_Metrics", exist_ok=True)
            plt.savefig("KPI/Revenue_Metrics/revenue_by_source.png")

            logging.info("Saving KPI metrics to KPI/Revenue_Metrics.csv")
            
            kpi = {
                "total_revenue": total_revenue,
                "total_order": total_order,
                "total_quantity_sold": total_quantity_sold,
                "Average_Order_Value": Average_Order_Value,
                "revenue_by_amazon": df[df["source"]=="Amazon"]["revenue"].sum(),
                "revenue_by_international": df[df["source"]=="International"]["revenue"].sum()
            }

            kpi_df = pd.DataFrame([kpi])
            
            kpi_df.to_csv("KPI/Revenue_Metrics/Revenue_Metrics.csv", index=False)
            
            # monthly data analysis
            logging.info("Generating monthly analysis")
            
            os.makedirs("KPI/Monthly_Analysis", exist_ok=True)
            logging.info("Saving monthly analysis plots to KPI/Monthly_Analysis/")
            
            
            plt.figure(figsize=(16,12))
            monthly_revenue = df.groupby('month')['revenue'].sum()
            monthly_revenue.to_csv("KPI/Monthly_Analysis/monthly_revenue.csv")
            plt.subplot(2, 2, 1)
            monthly_revenue.plot(kind='bar', title='Monthly Revenue')
            plt.xlabel('Month')
            plt.ylabel('Revenue')
            plt.tight_layout()

            ## monthly quantity sold
            monthly_quantity_sold = df.groupby('month')['quantity'].sum()
            plt.subplot(2, 2, 2)
            monthly_quantity_sold.to_csv("KPI/Monthly_Analysis/monthly_quantity_sold.csv")
            monthly_quantity_sold.plot(kind='bar', title='Monthly Quantity Sold')
            plt.xlabel('Month')
            plt.ylabel('Quantity Sold')
            plt.tight_layout()

            # monthly growth
            monthly_growth = monthly_revenue.pct_change() * 100
            monthly_growth.to_csv("KPI/Monthly_Analysis/monthly_growth.csv")
            plt.subplot(2, 2, 3)
            monthly_growth.plot(kind='bar', title='Monthly Growth (%)')
            plt.xlabel('Month')
            plt.ylabel('Growth (%)')
            plt.tight_layout()
            



            # Revenue Trend Line
            plt.subplot(2, 2, 4)
            monthly_revenue.plot(kind='line', title='Revenue Trend Over Months')
            plt.xlabel('Month')
            plt.ylabel('Revenue')
            plt.savefig("KPI/Monthly_Analysis/revenue_trend.png")
            plt.tight_layout()
            
            logging.info("Correlation matrix generation completed successfully")
            
            logging.info("Creating directory for Product Analytics at KPI/Product Analytics")
            os.makedirs('KPI/Product Analytics', exist_ok=True)
            
            # top 10 SKUs by Revenue
            top_skus = df.groupby('sku')['revenue'].sum().sort_values(ascending=False).head(10)
            top_skus
            top_skus.to_csv("KPI/Product Analytics/top_skus_by_revenue.csv")
            plt.figure(figsize=(15,10))
            plt.subplot(2,2,1)
            top_skus.plot(kind='bar', title='Top 10 SKUs by Revenue')
            plt.xlabel('SKU')
            plt.ylabel('Revenue')
            plt.tight_layout()

            # Top 10 SKUs by Quantity

            top_skus_quantity = df.groupby('sku')['quantity'].sum().sort_values(ascending=False).head(10)
            top_skus_quantity.to_csv("KPI/Product Analytics/top_skus_by_quantity.csv")
            plt.subplot(2,2,2)
            top_skus_quantity.plot(kind='bar', title='Top 10 SKUs by Quantity Sold')
            plt.xlabel('SKU')
            plt.ylabel('Quantity Sold')
            plt.tight_layout()

            # Product Revenue Contribution %
            product_revenue_contribution = (df.groupby('sku')['revenue'].sum() / df['revenue'].sum()) * 100
            product_revenue_contribution = product_revenue_contribution.sort_values(ascending=False).head(10)
            product_revenue_contribution.to_csv("KPI/Product Analytics/product_revenue_contribution.csv")
            plt.subplot(2,2,3)
            product_revenue_contribution.plot(kind='bar', title='Top 10 SKUs by Revenue Contribution (%)')
            plt.xlabel('SKU')
            plt.ylabel('Revenue Contribution (%)')
            plt.tight_layout()


            # Pareto Analysis (80/20 Rule)

            cumulative_revenue = df.groupby('sku')['revenue'].sum().sort_values(ascending=False).cumsum()
            cumulative_revenue_percentage = (cumulative_revenue / df['revenue'].sum())
            pareto_skus = cumulative_revenue_percentage[cumulative_revenue_percentage <= 0.8].index

            pd.Series(pareto_skus).to_csv("KPI/Product Analytics/pareto_skus.csv", index=False)
            plt.subplot(2,2,4)
            cumulative_revenue_percentage.plot(kind='line', title='Cumulative Revenue Percentage (Pareto Analysis)')
            plt.xlabel('SKU')
            plt.ylabel('Cumulative Revenue Percentage')
            plt.tight_layout()
            
            plt.savefig('KPI/Product Analytics/product_analytics.jpg')

            
            os.makedirs("KPI/Geographic_Analysis", exist_ok=True)
            logging.info("Saving geographic analysis plots to KPI/Geographic_Analysis/")
            
            # Revenue by Country
            revenue_by_country = df.groupby('country')['revenue'].sum().sort_values(ascending=False)
            revenue_by_country.to_csv("KPI/Geographic_Analysis/revenue_by_country.csv")
            plt.figure(figsize=(12,8))
            plt.subplot(2,2,1)

            revenue_by_country.plot(kind='bar', title='Revenue by Country')
            plt.xlabel('Country')
            plt.ylabel('Revenue')
            plt.tight_layout()

            # Quantity by Country

            quantity_by_country = df.groupby('country')['quantity'].sum().sort_values(ascending=False)
            quantity_by_country.to_csv("KPI/Geographic_Analysis/quantity_by_country.csv")
            plt.subplot(2,2,2)
            quantity_by_country.plot(kind='bar', title='Quantity Sold by Country')
            plt.xlabel('Country')
            plt.ylabel('Quantity Sold')
            plt.tight_layout()


            # Revenue % Contribution by Country

            revenue_percentage_by_country = (df.groupby('country')['revenue'].sum() / df['revenue'].sum()) * 100
            revenue_percentage_by_country = revenue_percentage_by_country.sort_values(ascending=False)
            revenue_percentage_by_country.to_csv("KPI/Geographic_Analysis/revenue_percentage_by_country.csv")
            plt.subplot(2,2,3)
            revenue_percentage_by_country.plot(kind='bar', title='Revenue % Contribution by Country')
            plt.xlabel('Country')
            plt.ylabel('Revenue % Contribution')
            plt.tight_layout()
            
            plt.savefig('KPI/Geographic_Analysis/geographic_analysis.jpg')
            
            # Advanced Analytical Features
            os.makedirs("KPI/Advanced_Analytical_Features", exist_ok=True)
            logging.info("Saving advanced analytical features plots to KPI/Advanced_Analytical_Features/")
            
            # Revenue per Day of Week
            df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
            df['day_of_week'] = df['order_date'].dt.day_name()
            revenue_by_day_of_week = df.groupby('day_of_week')['revenue'].sum().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
            revenue_by_day_of_week.to_csv("KPI/Advanced_Analytical_Features/revenue_by_day_of_week.csv")
            plt.figure(figsize=(10,6))
            revenue_by_day_of_week.plot(kind='bar', title='Revenue by Day of Week')
            plt.xlabel('Day of Week')
            plt.ylabel('Revenue')
            plt.tight_layout()
            plt.savefig("KPI/Advanced_Analytical_Features/revenue_by_day_of_week.png")


            # Rolling 7-Day Revenue
            df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
            daily_revenue = df.groupby('order_date')['revenue'].sum()
            rolling_7_day_revenue = daily_revenue.rolling(window=7).mean()
            rolling_7_day_revenue.to_csv("KPI/Advanced_Analytical_Features/rolling_7_day_revenue.csv")
            plt.figure(figsize=(12,6))
            rolling_7_day_revenue.plot(kind='line', title='Rolling 7-Day Average Revenue')
            plt.xlabel('Date')
            plt.ylabel('Rolling 7-Day Average Revenue')
            plt.tight_layout()
            plt.savefig("KPI/Advanced_Analytical_Features/rolling_7_day_revenue.png")

            # Revenue Distribution

            plt.figure(figsize=(10,6))
            plt.subplot(2,2,1)
            df['revenue'].plot(kind='hist', bins=30, title='Revenue Distribution')
            plt.xlabel('Revenue')
            plt.ylabel('Frequency')
            plt.subplot(2,2,2)
            df['revenue'].plot(kind='box', title='Revenue Box Plot')
            plt.ylabel('Revenue')
            plt.tight_layout()
            plt.savefig("KPI/Advanced_Analytical_Features/revenue_distribution.png")

            # Top 20% SKUs Contribution

            cumulative_revenue = df.groupby('sku')['revenue'].sum().sort_values(ascending=False).cumsum()
            cumulative_revenue_percentage = cumulative_revenue / df['revenue'].sum()
            top_20_percent_skus = cumulative_revenue_percentage[cumulative_revenue_percentage <= 0.2].index
            pd.Series(top_20_percent_skus).to_csv("KPI/Advanced_Analytical_Features/top_20_percent_skus.csv", index=False)
            



            
        except Exception as e:
            logging.error("Error in generating correlation matrix: {0}".format(str(e)))