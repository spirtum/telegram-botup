from .base import StringConstant


class UpdateType(StringConstant):
    pass


CALLBACK_QUERY = UpdateType('callback_query')
INLINE_QUERY = UpdateType('inline_query')
CHANNEL_POST = UpdateType('channel_post')
EDITED_MESSAGE = UpdateType('edited_message')
EDITED_CHANNEL_POST = UpdateType('edited_channel_post')
CHOSEN_INLINE_RESULT = UpdateType('chosen_inline_result')
SHIPPING_QUERY = UpdateType('shipping_query')
PRE_CHECKOUT_QUERY = UpdateType('pre_checkout_query')
POLL = UpdateType('poll')
POLL_ANSWER = UpdateType('poll_answer')
MESSAGE_POLL = UpdateType('message_poll')
MESSAGE_COMMAND = UpdateType('message_command')
MESSAGE_TEXT = UpdateType('message_text')
MESSAGE_DICE = UpdateType('message_dice')
MESSAGE_DOCUMENT = UpdateType('message_document')
MESSAGE_ANIMATION = UpdateType('message_animation')
MESSAGE_AUDIO = UpdateType('message_audio')
MESSAGE_CONTACT = UpdateType('message_contact')
MESSAGE_GAME = UpdateType('message_game')
MESSAGE_INVOICE = UpdateType('message_invoice')
MESSAGE_LEFT_CHAT_MEMBER = UpdateType('message_left_chat_member')
MESSAGE_LOCATION = UpdateType('message_location')
MESSAGE_NEW_CHAT_MEMBERS = UpdateType('message_new_chat_members')
MESSAGE_NEW_CHAT_PHOTO = UpdateType('message_new_chat_photo')
MESSAGE_NEW_CHAT_TITLE = UpdateType('message_new_chat_title')
MESSAGE_PHOTO = UpdateType('message_photo')
MESSAGE_STICKER = UpdateType('message_sticker')
MESSAGE_SUCCESSFUL_PAYMENT = UpdateType('message_successful_payment')
MESSAGE_VENUE = UpdateType('message_venue')
MESSAGE_VIDEO = UpdateType('message_video')
MESSAGE_VIDEO_NOTE = UpdateType('message_video_note')
MESSAGE_VOICE = UpdateType('message_voice')
