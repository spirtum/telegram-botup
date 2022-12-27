import logging


def get_logger():
    return logging.getLogger('botup')


def setup_logging(level=logging.INFO):
    logger = logging.getLogger('botup')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(level)
