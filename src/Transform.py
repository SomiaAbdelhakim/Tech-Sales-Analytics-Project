import pandas as pd
from src.Logger import logger, log_execution_time

class DataTransformer:
    """
    Performs all transformations required before
    building dimensions and fact tables.
    """

    def __init__(self, config):

        self.config = config

    @log_execution_time
    def transform_sales(self, sales_df: pd.DataFrame,) -> pd.DataFrame:
        """
        Transform Sales dataset.
        """
        logger.info("Transforming Sales data...")
        df = sales_df.copy()

        df = self._parse_dates(df)

        df = self._cast_numeric_columns(
            df,df.select_dtypes(include=['number'])
            )

        df = self._standardise_strings(df)

        df = self._remove_duplicates(df)

        df = self._standardize_country_names(df)

        df = self._remove_invalid_dates(df)

        df = self._remove_future_dates(df)

        df = self._remove_invalid_quantity(df)

        df = self._remove_negative_prices(df)

        df = self._fill_nulls(df, self.config.Sales_Null_Defaults)

        df = self._calculate_sales_amount(df)
        
        df = self._extract_color_from_product_name(df)
        
        df = self._parse_String(df)



        logger.info("Sales transformation completed.")
        return df

    @log_execution_time
    def transform_forecast(self, forecast_df: pd.DataFrame,) -> pd.DataFrame:
        """
        Transform Forecast dataset.
        """
        logger.info("Transforming Forecast data...")
        df = forecast_df.copy()

        df = self._cast_numeric_columns(
            df, df.select_dtypes(include=['number'])
            )

        df = self._standardise_strings(df)

        df = self._fill_nulls(df, self.config.Forecast_Null_Defaults)
        
        df = self._remove_duplicates(df)

        df = self._standardize_country_names(df)

        logger.info("Forecast transformation completed.")

        return df

    # ==========================================================
    # Methods
    # ==========================================================

    def _parse_dates(self, df: pd.DataFrame,) -> pd.DataFrame:
        """
        Convert OrderDate to datetime.
        """
        df["OrderDate"] = pd.to_datetime(
            df["OrderDate"],
            errors="coerce",
        )

        return df
    
    def _parse_String(self, df: pd.DataFrame,) -> pd.DataFrame:
        """
        Convert OrderDate to datetime.
        """
        df["Customer Code"] = (
            df["Customer Code"]
            .astype("string")
            .str.strip()
        )
        return df

    def _cast_numeric_columns(self, df: pd.DataFrame, columns: dict,) -> pd.DataFrame:
        """
        Convert columns to numeric types.
        """

        for column in columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )

        return df

    def _standardise_strings(self, df: pd.DataFrame, ) -> pd.DataFrame:
        """
        Trim whitespace and standardize text columns.
        """
        string_columns = df.select_dtypes(
                include=["object", "string"]
            ).columns

        for col in string_columns:
            df[col] = (
                df[col].astype("string").str.strip()
                )
        return df
    
    def _standardize_country_names(self, df):

        if "CountryRegion" in df.columns:

            df["CountryRegion"] = (
                df["CountryRegion"]
                .replace(self.config.COUNTRY_MAPPING)
            )

        return df

    def _remove_duplicates(self, df):

        before = len(df)

        df = df.drop_duplicates()

        removed = before - len(df)

        if removed:

            logger.warning(
                "Removed %d duplicate rows.",
                removed
            )

        return df

    def _fill_nulls(self, df: pd.DataFrame, null_defaults: dict) -> pd.DataFrame:
        """
        Replace missing values.
        """
        for column, value in null_defaults.items():

            if column in df.columns:

                df[column] = df[column].fillna(value)

        return df


    def _remove_invalid_quantity(self, df):
        if "Quantity" not in df.columns:
            return df

        before = len(df)

        df = df[df["Quantity"] > 0]

        removed = before - len(df)
        if removed:

            logger.warning(
                "Removed %d rows with invalid quantity.",
                removed
            )

        return df
    
    def _remove_negative_prices(self, df):

        price_columns = [
            "Unit Price",
            "Unit Cost",
            "Net Price"
        ]

        before = len(df)

        for col in price_columns:

            if col in df.columns:

                df = df[df[col] >= 0]

        removed = before - len(df)

        if removed:

            logger.warning(
                "Removed %d rows with negative prices.",
                removed
            )

        return df

    def _remove_invalid_dates(self, df):

        if "OrderDate" not in df.columns:
            return df

        before = len(df)

        df = df[df["OrderDate"].notna()]

        removed = before - len(df)

        if removed:

            logger.warning(
                "Removed %d rows with invalid dates.",
                removed
            )

        return df

    def _remove_future_dates(self, df):

        if "OrderDate" not in df.columns:
            return df

        today = pd.Timestamp.today().normalize()

        before = len(df)

        df = df[df["OrderDate"] <= today]

        removed = before - len(df)

        if removed:

            logger.warning(
                "Removed %d rows with future dates.",
                removed
            )

        return df
    
    def _calculate_sales_amount(self, df: pd.DataFrame,) -> pd.DataFrame:
        """
        Calculate SalesAmount.
        """
        df["SalesAmount"] = (
            df["Quantity"]
            * df["Net Price"]
        )
        return df
    
    def _extract_color_from_product_name(self, df: pd.DataFrame) -> pd.DataFrame:
 
        if "Product Name" not in df.columns:
            logger.warning("'Product Name' column not found — Color not updated.")
            return df
 
        # Read valid colors from Config and apply title case
        valid_colors = {c.title() for c in self.config.VALID_COLORS}
 
        split = df["Product Name"].str.strip().str.rsplit(n=1, expand=True)
 
        name_without_color = split[0]          
        last_word          = split[1].str.title()  
 
        is_color = last_word.isin(valid_colors)
 
        df["Color"] = last_word.where(is_color, "N/A")
 
        df["Product Name"] = name_without_color.where(
            is_color,
            df["Product Name"],   
        )
 
        extracted = int(is_color.sum())
        not_found = int((~is_color).sum())
 
        logger.info(
            "  Color extracted from Product Name: %d product(s) updated | "
            "%d product(s) have no color in name → set to 'N/A'.",
            extracted,
            not_found,
        )
 
        return df