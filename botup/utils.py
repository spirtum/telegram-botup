from .core.utils import get_logger, setup_logging, get_chat_id

__all__ = [
    'get_logger',
    'setup_logging',
    'get_chat_id',
    'start_group_link',
    'start_link'
]


def start_group_link(bot_name: str):
    return f'https://telegram.me/{bot_name}?startgroup='


def start_link(bot_name: str):
    return f'https://telegram.me/{bot_name}?start='
