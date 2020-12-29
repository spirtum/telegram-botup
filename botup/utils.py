import logging

try:
    import ujson as json
except ImportError:
    import json

from .types import (
    User,
    Chat,
    Poll,
    File,
    Update,
    Message,
    ChatMember,
    StickerSet,
    BotCommand,
    WebhookInfo,
    RawResponse,
    ErrorResponse,
    GameHighScore,
    UserProfilePhotos
)


def get_logger():
    return logging.getLogger('botup')


def setup_logging(level=logging.INFO):
    logger = logging.getLogger('botup')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(level)


def parse_response(response):
    if not isinstance(response, dict):
        response = json.loads(response)
    status = response.get('ok')
    result = response.get('result')
    if not status:
        return ErrorResponse(**response)
    elif isinstance(result, bool) or isinstance(result, str):
        return RawResponse(**response)
    elif isinstance(result, list):
        parsed_result = []
        for item in result:
            if 'update_id' in item:
                parsed_result.append(Update(**item))
            elif 'command' in item:
                parsed_result.append(BotCommand(**item))
            elif 'user' in item and 'status' in item:
                parsed_result.append(ChatMember(**item))
            elif 'user' in item and 'score' in item:
                parsed_result.append(GameHighScore(**item))
        return parsed_result
    elif 'update_id' in result:
        return Update(**result)
    elif 'message_id' in result:
        return Message(**result)
    elif 'is_bot' in result:
        return User(**result)
    elif 'total_count' in result and 'photos' in result:
        return UserProfilePhotos(**result)
    elif 'file_id' in result and 'file_size' in result and 'file_path' in result:
        return File(**result)
    elif 'type' in result and result['type'] in ('private', 'group', 'supergroup', 'channel'):
        return Chat(**result)
    elif 'user' in result and 'status' in result:
        return ChatMember(**result)
    elif 'question' in result and 'options' in result:
        return Poll(**result)
    elif 'contains_masks' in result and 'stickers' in result:
        return StickerSet(**result)
    elif 'has_custom_certificate' in result:
        return WebhookInfo(**result)
    else:
        return result


def error_response(text):
    return json.dumps({'ok': False, 'error_code': 502, 'description': text})


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
