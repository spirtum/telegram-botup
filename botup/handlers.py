from .mixins import HandlerPatternMixin, HandlerSimpleMixin


class AnimationHandler(HandlerSimpleMixin):
    pass


class AudioHandler(HandlerSimpleMixin):
    pass


class CallbackQueryHandler(HandlerPatternMixin):

    def __init__(self, update, user_handlers):
        super().__init__(update, user_handlers)

    def handle(self):
        handler = self.get_handler(self.update.callback_query.data)
        handler(self.update.callback_query.message.chat.id, self.update) if handler else None


class ChannelPostHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)

    def handle(self):
        if not self.user_handler:
            return
        self.user_handler(self.update.channel_post.chat.id, self.update)


class ChosenInlineResultHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)

    def handle(self):
        if not self.user_handler:
            return
        self.user_handler(self.update.chosen_inline_result.from_.id, self.update)


class CommandHandler(HandlerPatternMixin):

    def __init__(self, update, user_handlers):
        super().__init__(update, user_handlers)

    def handle(self):
        handler = self.get_handler(self.update.message.text)
        handler(self.update.message.chat.id, self.update) if handler else None


class ConnectedWebsiteHandler(HandlerSimpleMixin):
    pass


class ContactHandler(HandlerSimpleMixin):
    pass


class DocumentHandler(HandlerSimpleMixin):
    pass


class EditedChannelPostHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)

    def handle(self):
        if not self.user_handler:
            return
        self.user_handler(self.update.edited_channel_post.chat.id, self.update)


class EditedMessageHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)

    def handle(self):
        if not self.user_handler:
            return
        self.user_handler(self.update.edited_message.chat.id, self.update)


class GameHandler(HandlerSimpleMixin):
    pass


class InlineQueryHandler(HandlerPatternMixin):

    def __init__(self, update, user_handlers):
        super().__init__(update, user_handlers)

    def handle(self):
        handler = self.get_handler(self.update.inline_query.query)
        handler(self.update.inline_query.from_.id, self.update) if handler else None


class InvoiceHandler(HandlerSimpleMixin):
    pass


class LeftChatMemberHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)


class LocationHandler(HandlerSimpleMixin):
    pass


class MessageHandler(HandlerPatternMixin):

    def __init__(self, update, user_handlers):
        super().__init__(update, user_handlers)

    def handle(self):
        handler = self.get_handler(self.update.message.text)
        handler(self.update.message.chat.id, self.update) if handler else None


class NewChatMembersHandler(HandlerSimpleMixin):
    pass


class NewChatPhotoHandler(HandlerSimpleMixin):
    pass


class NewChatTitleHandler(HandlerSimpleMixin):
    pass


class PassportDataHandler(HandlerSimpleMixin):
    pass


class PhotoHandler(HandlerSimpleMixin):
    pass


class PollHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)

    def handle(self):
        if not self.user_handler:
            return
        self.user_handler(None, self.update)


class PreCheckoutQueryHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)

    def handle(self):
        if not self.user_handler:
            return
        self.user_handler(self.update.pre_checkout_query.from_.id, self.update)


class ShippingQueryHandler(HandlerSimpleMixin):

    def __init__(self, update, user_handler):
        super().__init__(update, user_handler)

    def handle(self):
        if not self.user_handler:
            return
        self.user_handler(self.update.shipping_query.from_.id, self.update)


class StickerHandler(HandlerSimpleMixin):
    pass


class SuccessfulPaymentHandler(HandlerSimpleMixin):
    pass


class VenueHandler(HandlerSimpleMixin):
    pass


class VideoHandler(HandlerSimpleMixin):
    pass


class VideoNoteHandler(HandlerSimpleMixin):
    pass


class VoiceHandler(HandlerSimpleMixin):
    pass
