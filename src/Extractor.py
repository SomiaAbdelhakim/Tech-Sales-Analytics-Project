import json
from pathlib import Path
from typing import Any
import pandas as pd
from src.Logger import logger, log_execution_time

class DataExtractor:

    def __init__(self, config,):

        self.config = config

    @log_execution_time
    def extract_sales(self) -> pd.DataFrame:
        """Load and validate the sales JSON file.

        Returns:
            Raw sales DataFrame (no transformation applied).

        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file is not valid JSON.
            ValueError: If required columns are missing.
        """
        sales_path = Path(self.config.SALES_FILE)

        logger.info("Extracting sales data from: %s", sales_path)

        Raw_Sales = self._load_json(sales_path)
        Sales_df = pd.DataFrame(Raw_Sales)

        if Sales_df is None or Sales_df.empty:
            raise ValueError("Sales DataFrame must not be None or empty.")
        
        logger.info("  Shape:      %s", Sales_df.shape)
        logger.info("  Duplicates: %d", Sales_df.duplicated().sum())
        logger.info("Extracted %d sales records | columns: %s", len(Sales_df), list(Sales_df.columns))
        return Sales_df

    @log_execution_time
    def extract_forecast(self) -> pd.DataFrame:
        """Load and validate the forecast JSON file.

        Returns:
            Raw forecast DataFrame (no transformation applied).

        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file is not valid JSON.
            ValueError: If required columns are missing.
        """
        forecast_path = Path(self.config.FORECAST_FILE)
        logger.info("Extracting forecast data from: %s", forecast_path)
        
        Forecast_raw = self._load_json(forecast_path)
        Forecast_df = pd.DataFrame(Forecast_raw)

        if Forecast_df is None or Forecast_df.empty:
            raise ValueError("Forecast DataFrame must not be None or empty.")

        logger.info("  Shape:      %s", Forecast_df.shape)
        logger.info("  Duplicates: %d", Forecast_df.duplicated().sum())
        logger.info("✓ Extracted %d forecast records | columns: %s",
                    len(Forecast_df), list(Forecast_df.columns))
 
        return Forecast_df


    @staticmethod
    def _load_json(path: Path) -> list[dict[str, Any]]:
        """Read a JSON file and return its contents.

        Args:
            path: Path object pointing to the JSON file.

        Returns:
            Parsed JSON content (expected to be a list of records).

        Raises:
            FileNotFoundError: Path does not exist.
            json.JSONDecodeError: Content is not valid JSON.
        """
        if not path.exists():
            raise FileNotFoundError(f"Source file not found: {path}")
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)


