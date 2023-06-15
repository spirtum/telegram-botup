from typing import Dict, Optional, Union, Pattern

from botup.types import Update, HandleFunction, BaseContext


class Handler:

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return None

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return None


class PatternHandler(Handler):

    def __init__(self):
        self._handlers: Dict[Union[str, Pattern], HandleFunction] = {}

    def register(self, pattern: Union[str, Pattern], function: HandleFunction):
        self._handlers[pattern] = function

    def get_handler(self, key: str) -> Optional[HandleFunction]:
        if key in self._handlers:
            return self._handlers[key]

        for pattern in self._handlers.keys():
            if isinstance(pattern, Pattern) and pattern.match(key):
                return self._handlers[pattern]

    async def handle(self, context: BaseContext):
        handler = self.get_handler(self.get_key(context.update))

        if not handler:
            return

        context.chat_id = self.get_chat_id(context.update)
        context.user_id = self.get_user_id(context.update)

        await handler(context)

    @staticmethod
    def get_key(update: Update) -> str:
        raise NotImplemented


class SimpleHandler(Handler):

    def __init__(self):
        self._handler: Optional[HandleFunction] = None

    def register(self, function: HandleFunction):
        self._handler = function

    async def handle(self, context: BaseContext):
        if not self._handler:
            return

        context.chat_id = self.get_chat_id(context.update)
        context.user_id = self.get_user_id(context.update)

        await self._handler(context)


class MessageAnimationHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class MessageAudioHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class CallbackQueryHandler(PatternHandler):

    @staticmethod
    def get_key(update: Update) -> str:
        return update.callback_query.data

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.callback_query.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.callback_query.from_.id


class ChannelPostHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.channel_post.chat.id


class ChosenInlineResultHandler(SimpleHandler):

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.chosen_inline_result.from_.id


class MessageCommandHandler(PatternHandler):

    @staticmethod
    def get_key(update: Update) -> str:
        return update.message.text

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class MessageContactHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class MessageDiceHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class MessageDocumentHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class EditedChannelPostHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.edited_channel_post.chat.id


class EditedMessageHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.edited_message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.edited_message.from_.id


class MessageGameHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class InlineQueryHandler(PatternHandler):

    @staticmethod
    def get_key(update: Update) -> str:
        return update.inline_query.query

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.inline_query.from_.id


class MessageInvoiceHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class MessageLeftChatMemberHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class MessageLocationHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class MessageTextHandler(PatternHandler):

    @staticmethod
    def get_key(update: Update) -> str:
        return update.message.text

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class MessageNewChatMembersHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class MessageNewChatPhotoHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class MessageNewChatTitleHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class MessagePhotoHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class PollHandler(SimpleHandler):
    pass


class MessagePollHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class PollAnswerHandler(SimpleHandler):

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.poll_answer.user.id


class PreCheckoutQueryHandler(SimpleHandler):

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.pre_checkout_query.from_.id


class ShippingQueryHandler(SimpleHandler):

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.shipping_query.from_.id


class MessageStickerHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class MessageSuccessfulPaymentHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class MessageVenueHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class MessageVideoHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class MessageVideoNoteHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id


class MessageVoiceHandler(SimpleHandler):

    @staticmethod
    def get_chat_id(update: Update) -> Optional[int]:
        return update.message.chat.id

    @staticmethod
    def get_user_id(update: Update) -> Optional[int]:
        return update.message.from_.id
