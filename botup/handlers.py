from .mixins import HandlerPatternMixin, HandlerSimpleMixin


class AnimationHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class AudioHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class CallbackQueryHandler(HandlerPatternMixin):

    def __init__(self, update, user_handlers):
        super().__init__(update, user_handlers)

    def handle(self):
        handler = self.get_handler(self.update.callback_query.data)
        handler(chat_id=self.update.callback_query.message.chat.id, update=self.update) if handler else None


class ChannelPostHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)

    def handle(self):
        if not self.user_handler:
            return
        self.user_handler(chat_id=self.update.channel_post.chat.id, update=self.update)


class ChosenInlineResultHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)

    def handle(self):
        if not self.user_handler:
            return
        self.user_handler(chat_id=self.update.chosen_inline_result.from_.id, update=self.update)


class CommandHandler(HandlerPatternMixin):

    def __init__(self, update, user_handlers):
        super().__init__(update, user_handlers)

    def handle(self):
        handler = self.get_handler(self.update.message.text)
        handler(chat_id=self.update.message.chat.id, update=self.update) if handler else None


class ConnectedWebsiteHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class ContactHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class DocumentHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class EditedChannelPostHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)

    def handle(self):
        if not self.user_handler:
            return
        self.user_handler(chat_id=self.update.edited_channel_post.chat.id, update=self.update)


class EditedMessageHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)

    def handle(self):
        if not self.user_handler:
            return
        self.user_handler(chat_id=self.update.edited_message.chat.id, update=self.update)


class GameHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class InlineQueryHandler(HandlerPatternMixin):

    def __init__(self, update, user_handlers):
        super().__init__(update, user_handlers)

    def handle(self):
        handler = self.get_handler(self.update.inline_query.query)
        handler(chat_id=self.update.inline_query.from_.id, update=self.update) if handler else None


class InvoiceHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class LeftChatMemberHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class LocationHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class MessageHandler(HandlerPatternMixin):

    def __init__(self, update, user_handlers):
        super().__init__(update, user_handlers)

    def handle(self):
        handler = self.get_handler(self.update.message.text)
        handler(chat_id=self.update.message.chat.id, update=self.update) if handler else None


class NewChatMembersHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class NewChatPhotoHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class NewChatTitleHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class PassportDataHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class PhotoHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class PollHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)

    def handle(self):
        if not self.user_handler:
            return
        self.user_handler(chat_id=None, update=self.update)


class PreCheckoutQueryHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)

    def handle(self):
        if not self.user_handler:
            return
        self.user_handler(chat_id=self.update.pre_checkout_query.from_.id, update=self.update)


class ShippingQueryHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)

    def handle(self):
        if not self.user_handler:
            return
        self.user_handler(chat_id=self.update.shipping_query.from_.id, update=self.update)


class StickerHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class SuccessfulPaymentHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class VenueHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class VideoHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class VideoNoteHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class VoiceHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)
