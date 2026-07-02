
from pathlib import Path
from datetime import datetime

class Config:
    """Centralized configuration for the ETL pipeline."""

    # ==========================================================
    # Project Directories
    # ==========================================================

    BASE_DIR = Path(r'C:\Users\SomayaAbdelhakim\OneDrive - Orion360\Data Analytics Task\Sales Task')

    RUN_DATE = datetime.now().strftime("%d-%m-%Y")
    DATA_DIR = BASE_DIR / "Inputs"
    OUTPUT_DIR = BASE_DIR / "Output"/ RUN_DATE
    LOG_DIR = BASE_DIR / "Logs"/ RUN_DATE

    # ==========================================================
    # Input Files
    # ==========================================================

    SALES_FILE = DATA_DIR / "Sales.json"

    FORECAST_FILE = DATA_DIR / "forecast.json"

    # ==========================================================
    # Output Folders
    # ==========================================================

    DIMENSION_FOLDER = OUTPUT_DIR / "dimensions"

    FACT_FOLDER = OUTPUT_DIR / "facts"

    REPORT_FOLDER = OUTPUT_DIR / "reports"

    # ==========================================================
    # Logging
    # ==========================================================

    LOG_FILE = LOG_DIR / "etl.log"

    LOG_LEVEL = "INFO"

    # ==========================================================
    # ETL Settings
    # ==========================================================

    # dayofweek: Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
    WEEKEND_DAYS = [4, 5] 
    DATE_FORMAT = "%Y-%m-%d"

    CSV_ENCODING = "utf-8"

    # ==========================================================
    # Expected Schemas
    # ==========================================================

    Sales_Required_Columns = [

        "OrderDate",
        "CustomerKey",
        "Customer Code",
        "Name",
        "ProductKey",
        "Product Name",
        "Brand",
        "Category",
        "Subcategory",
        "Quantity",
        "Net Price",
        "CountryRegion",
        "State",
        "City",

    ]
    Fact_Sales_Final_Columns=[
     "ProductKey",
     "CustomerKey",
     "DateKey",
     "GeographyKey",
     "BrandKey",
     "Quantity",
     "Net Price",
     "SalesAmount",
     ]
    
    Forecast_Required_Columns = [
        "Year",
        "CountryRegion",
        "Brand",
        "Forecast",
    ]
    Fact_Forecast_Final_Columns=[
        "DateKey",
        "GeographyKey",
        "BrandKey",
        "Forecast",
    ]

    Sales_Null_Defaults = {

        "Name": "Unknown Customer",
        "Education": "Unknown",
        "Occupation": "Unknown",
        "City": "Unknown",
        "State": "Unknown",

    }

    Forecast_Null_Defaults = {
        "Country": "Unknown",
        "State": "Unknown",
        "Brand": "Unknown",
    }

    Sales_Amount = {
        "quantity": "Quantity",
        "price": "Net Price",
        "result": "SalesAmount",
        "round": 2,
    }

    # ---------------------------------------------------------------------------
    # Output table → CSV filename mapping
    # ---------------------------------------------------------------------------
    OUTPUT_TABLES = {

        "DIM_Product": "DIM_Product.csv",
        "DIM_Customer": "DIM_Customer.csv",
        "DIM_Date": "DIM_Date.csv",
        "DIM_Geography": "DIM_Geography.csv",
        "DIM_Brand": "DIM_Brand.csv",
        "FACT_Sales": "FACT_Sales.csv",
        "FACT_Forecast": "FACT_Forecast.csv",

    }
    # -----------------------------------------------------------------------------
    # Country Mapping
    # -----------------------------------------------------------------------------
    COUNTRY_MAPPING = {
        "USA": "United States",
        "U.S.A.": "United States",
        "US": "United States",
        "United States Of America": "United States",

        "UK": "United Kingdom",
        "U.K.": "United Kingdom",

        "UAE": "United Arab Emirates"
    }
    # -----------------------------------------------------------------------------
    # Dimensions
    # -----------------------------------------------------------------------------

    DIM_PRODUCT_COLUMNS=[
        "ProductKey", "Product Name", "Subcategory", "Category","Brand", "Color",]
    
    DIM_CUSTOMER_COLUMNS=["CustomerKey", "Customer Code", "Name", "Education",
              "Occupation", "Continent", "City", "State", "CountryRegion"]
    DIM_GEOGRAPHY_COLUMNS=["Continent", "CountryRegion", "State", "City"]
    DIM_BRAND_COLUMNS =["Brand"]

    # -------------------------------------------------------------------------------
    # Valid Colors
    # -------------------------------------------------------------------------------
    VALID_COLORS = {
    "Black", "White", "Silver", "Grey", "Gray",
    "Blue",  "Red",   "Green",  "Brown", "Pink",
    "Orange", "Yellow", "Gold", "Bronze", "Beige",
    "Purple", "Clear", "Transparent", "Multicolor","Azure",
    }