"""
main.py
--------
Entry point for the Sales Analytics ETL Pipeline.

Workflow
--------
1. Extract raw data
2. Validate source data
3. Transform and clean data
4. Build dimension tables
5. Build fact tables
6. Load CSV files
7. Log execution summary
"""
import time
import win32com.client as win32

from Config import Config
from src.Extractor import DataExtractor
from src.Validation import DataValidator
from src.Transform import DataTransformer
from src.Dimension import DimensionBuilder
from src.FactTables import FactBuilder
from src.Load import DataLoader
from src.Logger import logger, log_execution_time

@log_execution_time
def main() -> None:
    """
    Execute the complete ETL pipeline.
    """

    start_time = time.perf_counter()
    logger.info("=" * 80)
    logger.info("Tech Sales ETL Pipeline Started")
    logger.info("=" * 80)

    try:

    # =====================================================
    # Initialize
    # =====================================================

        config = Config()
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.Quit()
        # setup_logger(config.LOG_FILE)
        logger.info("=" * 60)
        logger.info("Sales Analytics ETL Pipeline Started")
        logger.info("=" * 60)

    # =====================================================
    # Extract
    # =====================================================

        logger.info("STEP 1 - Extracting data...")
        extractor = DataExtractor(config)
        sales_df = extractor.extract_sales()
        forecast_df = extractor.extract_forecast()

    # =====================================================
    # Validate Raw Data
    # =====================================================

        logger.info("STEP 2 - Validating raw data...")

        validator = DataValidator(config)

        validator.validate_sales(sales_df)

        validator.validate_forecast(forecast_df)

    # =====================================================
    # Transform
    # =====================================================

        logger.info("STEP 3 - Transforming data...")

        transformer = DataTransformer(config)

        sales_df = transformer.transform_sales(sales_df)

        forecast_df = transformer.transform_forecast(forecast_df)

        print(sales_df['CountryRegion'].unique())
        print(forecast_df['CountryRegion'].unique())
    # =====================================================
    # Build Dimensions
    # =====================================================

        logger.info("STEP 4 - Building dimensions...")

        dimension_builder = DimensionBuilder(config)

        dimensions = dimension_builder.build_dimensions(
            sales_df,
        )

    # =====================================================
    # Build Facts
    # =====================================================

        logger.info("STEP 5 - Building fact tables...")

        fact_builder = FactBuilder(
            config = config,
            sales_df=sales_df,
            forecast_df=forecast_df,
            dimensions=dimensions,
        )

        facts = fact_builder.build_fact_tables()

    # =====================================================
    # Load
    # =====================================================

        logger.info("STEP 6 - Saving output files...")

        loader = DataLoader(config)

        loader.save_dimensions(dimensions)

        loader.save_facts(facts)

    # Optional
    # loader.save_data_quality_report()

    # =====================================================
    # Finish
    # =====================================================

        execution_time = time.perf_counter() - start_time

        logger.info("=" * 60)
        logger.info("ETL Pipeline Completed Successfully")
        logger.info("Execution Time : %.2f seconds", execution_time)
        logger.info("=" * 60)

    except Exception:

        logger.exception("ETL Pipeline Failed.")

        raise


if __name__ == "__main__":
    main()