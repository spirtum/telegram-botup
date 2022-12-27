from typing import Dict, Optional, Union, Pattern

from .types import Update, HandleFunction, Context


class Handler:

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return None

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return None


class PatternHandler(Handler):

    def __init__(self, pattern: Pattern, function: HandleFunction):
        self.pattern = pattern
        self.function = function

    @classmethod
    def get_handler(
            cls,
            key: str,
            handlers: Dict[Union[str, Pattern], HandleFunction]
    ) -> Optional[HandleFunction]:

        if key in handlers:
            return handlers[key]

        for pattern in handlers.keys():
            if isinstance(pattern, Pattern) and pattern.match(key):
                return handlers[pattern]

    @classmethod
    async def handle(cls, context: Context, handlers: Dict[str, HandleFunction]) -> bool:
        handler = cls.get_handler(cls.get_key(context.update), handlers)

        if not handler:
            return False

        context.chat_id = cls.get_chat_id(context.update)
        context.user_id = cls.get_user_id(context.update)

        await handler(context)
        return True

    @classmethod
    def get_key(cls, update: Update) -> str:
        raise NotImplemented


class SimpleHandler(Handler):

    def __init__(self, function: HandleFunction):
        self.function = function

    @classmethod
    async def handle(cls, context: Context, handler: Optional[HandleFunction]) -> bool:
        if not handler:
            return False

        context.chat_id = cls.get_chat_id(context.update)
        context.user_id = cls.get_user_id(context.update)

        await handler(context)
        return True


class AnimationHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class AudioHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class CallbackQueryHandler(PatternHandler):

    @classmethod
    def get_key(cls, update: Update) -> str:
        return update.callback_query.data

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.callback_query.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.callback_query.from_.id


class ChannelPostHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.channel_post.chat.id


class ChosenInlineResultHandler(SimpleHandler):

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.chosen_inline_result.from_.id


class CommandHandler(PatternHandler):

    @classmethod
    def get_key(cls, update: Update) -> str:
        return update.message.text

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class ContactHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class DiceHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class DocumentHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class EditedChannelPostHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.edited_channel_post.chat.id


class EditedMessageHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.edited_message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class GameHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class InlineQueryHandler(PatternHandler):

    @classmethod
    def get_key(cls, update: Update) -> str:
        return update.inline_query.query

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.inline_query.from_.id


class InvoiceHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class LeftChatMemberHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class LocationHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class MessageHandler(PatternHandler):

    @classmethod
    def get_key(cls, update: Update) -> str:
        return update.message.text

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class NewChatMembersHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class NewChatPhotoHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class NewChatTitleHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class PhotoHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class MessagePollHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.poll.from_.id


class PollAnswerHandler(SimpleHandler):

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.poll_answer.user.id


class PreCheckoutQueryHandler(SimpleHandler):

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.pre_checkout_query.from_.id


class ShippingQueryHandler(SimpleHandler):

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.shipping_query.from_.id


class StickerHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class SuccessfulPaymentHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class VenueHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class VideoHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class VideoNoteHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id


class VoiceHandler(SimpleHandler):

    @classmethod
    def get_chat_id(cls, update: Update) -> Optional[int]:
        return update.message.chat.id

    @classmethod
    def get_user_id(cls, update: Update) -> Optional[int]:
        return update.message.from_.id
