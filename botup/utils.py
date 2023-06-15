import logging


__all__ = [
    'get_logger',
    'setup_logging',
    'start_group_link',
    'start_link'
]


def get_logger():
    return logging.getLogger('botup')


def setup_logging(level=logging.INFO):
    logger = logging.getLogger('botup')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(level)


def start_group_link(bot_name: str):
    return f'https://telegram.me/{bot_name}?startgroup='


def start_link(bot_name: str):
    return f'https://telegram.me/{bot_name}?start='
