from typing import Dict
import pandas as pd
from src.Logger import logger, log_execution_time

class FactBuilder:

    def __init__(
        self,
        sales_df: pd.DataFrame,
        forecast_df: pd.DataFrame,
        dimensions: Dict[str, pd.DataFrame],
        config
    ) -> None:
        self.config = config
        self._Fact_Sales_Final_Columns = config.Fact_Sales_Final_Columns
        self._Fact_Forecast_Final_Columns = config.Fact_Forecast_Final_Columns

        self.sales_df = sales_df.copy()
        self.forecast_df = forecast_df.copy()
        self.dimensions = dimensions

    # ==========================================================
    # Methods
    # ==========================================================

    def build_fact_tables(self) -> Dict[str, pd.DataFrame]:

        logger.info("Building fact tables...")

        fact_sales = self.build_fact_sales()

        fact_forecast = self.build_fact_forecast()

        logger.info("Fact tables created successfully.")

        return {
            "FACT_Sales": fact_sales,
            "FACT_Forecast": fact_forecast,
        }

    # ==========================================================
    # FACT SALES
    # ==========================================================
    @log_execution_time
    def build_fact_sales(self) -> pd.DataFrame:

        logger.info("Building FACT_Sales...")

        fact = self.sales_df.copy()

        # ------------------------------------------------------
        # DateKey
        # ------------------------------------------------------
        dim_date = self.dimensions["DIM_Date"][
            [
                "DateKey",
                "Date"]
        ]

        fact = fact.merge(
            dim_date,
            left_on="OrderDate",
            right_on="Date",
            how="left")

        fact.drop(columns="Date", inplace=True)

        # ------------------------------------------------------
        # GeographyKey
        # ------------------------------------------------------
        dim_geo = self.dimensions["DIM_Geography"][
            [
                "GeographyKey",
                "CountryRegion",
                "State",
                "City"]
        ]

        fact = fact.merge(
            dim_geo,
            on=[
                "CountryRegion",
                "State",
                "City"],
            how="left")

        # ------------------------------------------------------
        # BrandKey
        # ------------------------------------------------------
        dim_brand = self.dimensions["DIM_Brand"][
            [
                "BrandKey",
                "Brand"]
        ]

        fact = fact.merge(
            dim_brand,
            on="Brand",
            how="left")

        # ------------------------------------------------------
        # Sales Amount
        # ------------------------------------------------------
        fact["SalesAmount"] = (
            fact["Quantity"]
            * fact["Net Price"]
        )

        # ------------------------------------------------------
        # Keep only required columns
        # ------------------------------------------------------
        fact = fact[self._Fact_Sales_Final_Columns]

        self._validate_fact_sales(fact)

        logger.info(
            "FACT_Sales created (%d rows).",
            len(fact)
        )

        return fact

    # ==========================================================
    # FACT FORECAST
    # ==========================================================

    @log_execution_time
    def build_fact_forecast(self) -> pd.DataFrame:

        logger.info("Building FACT_Forecast...")

        fact = self.forecast_df.copy()

        # ------------------------------------------------------
        # Create Date Column
        # Forecast is yearly
        # ------------------------------------------------------

        fact["Date"] = pd.to_datetime(
            fact["Year"].astype(str) + "-01-01"
        )
        # ------------------------------------------------------
        # DateKey
        # ------------------------------------------------------
        dim_date = self.dimensions["DIM_Date"][
            [
                "DateKey",
                "Date"
            ]
        ]
        fact = fact.merge(
            dim_date,
            on="Date",
            how="left"
        )

        # ------------------------------------------------------
        # BrandKey
        # ------------------------------------------------------
        dim_brand = self.dimensions["DIM_Brand"][
            [
                "BrandKey",
                "Brand"
            ]
        ]

        fact = fact.merge(
            dim_brand,
            on="Brand",
            how="left"
        )
        # ------------------------------------------------------
        # GeographyKey
        # ------------------------------------------------------
        dim_geo =(
            self.dimensions["DIM_Geography"][
                ["GeographyKey", "CountryRegion"]
            ]
            .drop_duplicates(subset=["CountryRegion"])
            .reset_index(drop=True)
        )
 
        fact = fact.merge(
            dim_geo,
            left_on=["CountryRegion"],
            right_on=["CountryRegion"],
            how="left",
        )

        # ------------------------------------------------------
        # Final Columns
        # ------------------------------------------------------

        fact =  fact = fact[self._Fact_Forecast_Final_Columns].sort_values(by="GeographyKey", ascending=True)

        self._validate_fact_forecast(fact)
        logger.info(
            "FACT_Forecast created (%d rows).",
            len(fact)
        )
        return fact

    # ==========================================================
    # VALIDATION Methods
    # ==========================================================

    @staticmethod
    def _validate_fact_sales(
        fact: pd.DataFrame
    ) -> None:

        if fact["DateKey"].isna().any():
            raise ValueError(
                "FACT_Sales contains missing DateKey."
            )

        if fact["BrandKey"].isna().any():
            raise ValueError(
                "FACT_Sales contains missing BrandKey."
            )

        if fact["GeographyKey"].isna().any():
            raise ValueError(
                "FACT_Sales contains missing GeographyKey."
            )

        if (fact["Quantity"] <= 0).any():
            raise ValueError(
                "Invalid Quantity found."
            )

        if (fact["SalesAmount"] < 0).any():
            raise ValueError(
                "Invalid SalesAmount found."
            )

    @staticmethod
    def _validate_fact_forecast(
        fact: pd.DataFrame
    ) -> None:

        if fact["DateKey"].isna().any():
            raise ValueError(
                "FACT_Forecast contains missing DateKey."
            )

        if fact["BrandKey"].isna().any():
            raise ValueError(
                "FACT_Forecast contains missing BrandKey."
            )

        if fact["GeographyKey"].isna().any():
            raise ValueError(
                "FACT_Forecast contains missing GeographyKey."
            )

        if fact["Forecast"].isna().any():
            raise ValueError(
                "Forecast contains NULL values."
            )

        if (fact["Forecast"] < 0).any():
            raise ValueError(
                "Forecast contains negative values."
            )