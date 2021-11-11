import logging


def get_logger():
    return logging.getLogger('botup')


def setup_logging(level=logging.INFO):
    logger = logging.getLogger('botup')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(level)


def start_group_link(bot_name):
    return f'https://telegram.me/{bot_name}?startgroup='


def start_link(bot_name):
    return f'https://telegram.me/{bot_name}?start='


def get_chat_id(update):
    if update.message:
        return update.message.chat.id
    if update.callback_query:
        return update.callback_query.from_.id
    if update.inline_query:
        return update.inline_query.from_.id
    if update.chosen_inline_result:
        return update.chosen_inline_result.from_.id
    if update.poll_answer:
        return update.poll_answer.user.id
    if update.edited_message:
        return update.edited_message.chat.id
    if update.channel_post:
        return update.channel_post.chat.id
    if update.edited_channel_post:
        return update.edited_channel_post.chat.id
    if update.shipping_query:
        return update.shipping_query.from_.id
    if update.pre_checkout_query:
        return update.pre_checkout_query.from_.id
