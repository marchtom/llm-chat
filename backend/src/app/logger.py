import logging
import sys


def setup_logger(
        name: str,
        level: int = logging.INFO,
        format: str = '%(asctime)s [%(levelname)s] %(message)s',
    ) -> logging.Logger:
    """Function to setup logging configuration."""

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


logger = setup_logger('app')
