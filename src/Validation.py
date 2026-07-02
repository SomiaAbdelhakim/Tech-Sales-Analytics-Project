import pandas as pd
from src.Logger import logger, log_execution_time

class DataValidator:
    """
    Validate source datasets before transformation.
    """

    def __init__(self, config):

        self.config = config

    @log_execution_time
    def validate_sales(
        self,
        sales_df: pd.DataFrame,
    ) -> None:
        """
        Validate Sales dataset.
        """

        logger.info("Validating Sales dataset...")

        self._validate_required_columns(
            sales_df,
            self.config.Sales_Required_Columns,
            "Sales",
        )

        self._validate_not_empty(
            sales_df,
            "Sales",
        )

        self._validate_positive_values(
            sales_df,
            ["Quantity", "Net Price"],
        )

        self._validate_duplicate_rows(
            sales_df,
            ["CustomerKey"],
            "Sales",
        )

        logger.info("Sales validation completed.")

    @log_execution_time
    def validate_forecast(
        self,
        forecast_df: pd.DataFrame,
    ) -> None:
        """
        Validate Forecast dataset.
        """

        logger.info("Validating Forecast dataset...")

        self._validate_required_columns(
            forecast_df,
            self.config.Forecast_Required_Columns,
            "Forecast",
        )

        self._validate_not_empty(
            forecast_df,
            "Forecast",
        )

        self._validate_positive_values(
            forecast_df,
            ["Forecast"],
        )

        self._validate_duplicate_rows(
            forecast_df,
            ["Brand"],
            "Forecast",
        )

        logger.info("Forecast validation completed.")

    # ==========================================================
    # Methods
    # ==========================================================

    @staticmethod
    def _validate_required_columns(
        df: pd.DataFrame,
        required_columns: list[str],
        dataset: str,
    ) -> None:

        missing = set(required_columns) - set(df.columns)

        if missing:

            raise ValueError(
                f"{dataset}: Missing columns {sorted(missing)}"
            )

    @staticmethod
    def _validate_not_empty(
        df: pd.DataFrame,
        dataset: str,
    ) -> None:

        if df.empty:

            raise ValueError(
                f"{dataset} dataset is empty."
            )

    @staticmethod
    def _validate_positive_values(
        df: pd.DataFrame,
        columns: list[str],
    ) -> None:

        for column in columns:

            if column in df.columns:

                if (df[column] < 0).any():

                    raise ValueError(
                        f"Negative values found in '{column}'."
                    )

    @staticmethod
    def _validate_duplicate_rows(
        df: pd.DataFrame,
        subset: list[str],
        dataset: str,
    ) -> None:
        
        duplicates = df.duplicated(subset=subset).sum()
        if duplicates > 0:

            logger.warning(
                "%s contains %d duplicate rows.",
                dataset,
                duplicates,
            )