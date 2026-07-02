"""
Builds all star-schema dimension tables (DIM_*) from the cleaned sales & Forecast DataFrame.

Each dimension is built by a dedicated private method so they can be
tested, extended, or replaced independently.
"""
import pandas as pd
from src.Logger import logger, log_execution_time
  
class DimensionBuilder:
 
    def __init__(self, config) -> None:
        """
        Store the config object so every private method can read it.
 
        Args:
            config: Config class instance from Config.py.
        """
        self.config = config

        self._weekend_days = config.WEEKEND_DAYS  # [4, 5]  → Fri & Sat
 

    
    def build_dimensions(self, sales_df: pd.DataFrame) -> dict:
        """
        Build all dimension tables and return them as a dictionary.
        """
        logger.info("Building dimension tables...")
 
        dimensions = {
            "DIM_Product":   self._build_dim_product(sales_df),
            "DIM_Customer":  self._build_dim_customer(sales_df),
            "DIM_Date":      self._build_dim_date(sales_df),
            "DIM_Geography": self._build_dim_geography(sales_df),
            "DIM_Brand":     self._build_dim_brand(sales_df),
        }
        logger.info("All dimension tables built.")
        return dimensions
 
    @log_execution_time
    def _build_dim_product(self, df: pd.DataFrame) -> pd.DataFrame:

        cols = self.config.DIM_PRODUCT_COLUMNS
 
        dim = df[cols].drop_duplicates().sort_values(by="ProductKey", ascending=True).reset_index(drop=True)
 
        logger.info("  DIM_Product   : %d rows", len(dim))
        return dim
 
    @log_execution_time
    def _build_dim_customer(self, df: pd.DataFrame) -> pd.DataFrame:

        cols = self.config.DIM_CUSTOMER_COLUMNS
 
        # Guard: skip any column that doesn't exist in this dataset
        # (e.g. "Education" may be absent in some source files).
        cols = [c for c in cols if c in df.columns]
 
        dim = df[cols].drop_duplicates().sort_values(by="CustomerKey", ascending=True).reset_index(drop=True)
 
        logger.info("  DIM_Customer  : %d rows", len(dim))
        return dim

    @log_execution_time
    def _build_dim_date(self, df: pd.DataFrame) -> pd.DataFrame:

        date_range = pd.date_range(
            start=df['OrderDate'].min(),
            end=df['OrderDate'].max(),
            freq="D",
        )
 
        dim = pd.DataFrame({
            "DateKey":    range(1, len(date_range) + 1),
            "Date":       date_range,
            "Year":       date_range.year,
            "Month":      date_range.month,
            "MonthName":  date_range.strftime("%B"),
            "Quarter":    date_range.quarter,
            "DayOfWeek":  date_range.day_name(),
            "DayOfMonth": date_range.day,
            "WeekOfYear": date_range.isocalendar().week.values,
            "IsWeekend":  date_range.dayofweek.isin(self._weekend_days),
        })
 
        return dim
    
    @log_execution_time
    def _build_dim_geography(self, df: pd.DataFrame) -> pd.DataFrame:
  
        cols = self.config.DIM_GEOGRAPHY_COLUMNS
 
        dim = df[cols].drop_duplicates().reset_index(drop=True)
        dim.insert(0, "GeographyKey", range(1, len(dim) + 1))
 
        logger.info("  DIM_Geography : %d rows", len(dim))
        return dim
 
    @log_execution_time
    def _build_dim_brand(self, df: pd.DataFrame) -> pd.DataFrame:

        cols = self.config.DIM_BRAND_COLUMNS
 
        dim = df[cols].drop_duplicates().reset_index(drop=True)
        dim.insert(0, "BrandKey", range(1, len(dim) + 1))
 
        logger.info("  DIM_Brand     : %d rows", len(dim))
        return dim
 