from pathlib import Path
from typing import Dict
import pandas as pd
from src.Logger import logger, log_execution_time

class DataLoader:

    def __init__(self, config):

        self.config = config
        self.output_dir = Path(config.OUTPUT_DIR)
        self.dimension_dir = self.output_dir / "Dimensions"

        self.fact_dir = self.output_dir / "Facts"
        self._create_directories()

    @log_execution_time
    def save_dimensions(
        self,
        dimensions: Dict[str, pd.DataFrame],
    ) -> None:
        """
        Save all dimension tables.
        """

        logger.info("Saving dimension tables...")

        for table_name, dataframe in dimensions.items():

            self._save_csv(
                dataframe=dataframe,
                folder=self.dimension_dir,
                filename=f"{table_name}.csv",
            )

        logger.info("Dimension tables saved.")

    @log_execution_time
    def save_facts(
        self,
        facts: Dict[str, pd.DataFrame],
    ) -> None:
        """
        Save all fact tables.
        """

        logger.info("Saving fact tables...")

        for table_name, dataframe in facts.items():

            self._save_csv(
                dataframe=dataframe,
                folder=self.fact_dir,
                filename=f"{table_name}.csv",
            )

        logger.info("Fact tables saved.")

    # ==========================================================
    # Methods
    # ==========================================================

    def _save_csv(self,dataframe: pd.DataFrame, folder: Path, filename: str,) -> None:
        """
        Save a DataFrame to CSV.
        """
        output_path = folder / filename
        dataframe.to_csv(
            output_path,
            index=False,
            encoding="utf-8",
        )
        logger.info(
            "Saved %s (%d rows).",
            output_path.name,
            len(dataframe),
        )

    def _create_directories(self) -> None:

        self.dimension_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.fact_dir.mkdir(
            parents=True,
            exist_ok=True,
        )
