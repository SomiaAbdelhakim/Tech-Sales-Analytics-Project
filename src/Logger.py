import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from functools import wraps
from time import perf_counter
from datetime import datetime


from Config import Config
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")



def setup_logger(name: str = "ETL") -> logging.Logger:
    """
    Configure application logger.
    """
    
    log_dir = Path(Config.LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"{timestamp}-Logs.log"

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()


def log_execution_time(func):
    """
    Decorator that logs execution time of a function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        start = perf_counter()

        logger.info("Started: %s", func.__name__)

        try:
            result = func(*args, **kwargs)

            elapsed = perf_counter() - start

            logger.info(
                "Finished: %s (%.2f sec)",
                func.__name__,
                elapsed,
            )

            return result

        except Exception:

            logger.exception("Failed while executing %s", func.__name__)

            raise

    return wrapper