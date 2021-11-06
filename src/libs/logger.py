import logging
from logging.handlers import RotatingFileHandler


def create_logger(name=__name__):
    path = '/add/your/full/path/to/fitzRoyPy/logs/log_file_name.log'
    file_handler = RotatingFileHandler(path, maxBytes=2000000, backupCount=7)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    msg = "%(asctime)s | %(levelname)s | %(module)s | %(message)s"
    formatter = logging.Formatter(msg)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
