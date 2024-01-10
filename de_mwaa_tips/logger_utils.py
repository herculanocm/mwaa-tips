import logging
from sys import stdout
from de_mwaa_tips.custom_formatter_logger import CustomFormatter
from de_mwaa_tips.minimal_formatter_logger import MinimalFormatter

def get_logger(logger: logging.Logger = None, is_minimal: bool = True) -> logging.Logger:
    if logger is None:

        if is_minimal:
            handler = logging.StreamHandler(stdout)
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(MinimalFormatter())
        else:
            handler = logging.StreamHandler(stdout)
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(CustomFormatter())

        logger = logging.getLogger(__name__)

        if logger.hasHandlers():
            logger.removeHandler(handler)

        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    return logger