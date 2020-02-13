from .mixins import HandlerPatternMixin, HandlerSimpleMixin


class AnimationHandler(HandlerSimpleMixin):
    pass


class AudioHandler(HandlerSimpleMixin):
    pass


class CallbackQueryHandler(HandlerPatternMixin):

    @classmethod
    def handle(cls, update, handlers):
        handler = cls.get_handler(update.callback_query.data, handlers)
        handler(update.callback_query.message.chat.id, update) if handler else None


class ChannelPostHandler(HandlerSimpleMixin):

    @classmethod
    def handle(cls, update, handler):
        if not handler:
            return
        handler(update.channel_post.chat.id, update)


class ChosenInlineResultHandler(HandlerSimpleMixin):

    @classmethod
    def handle(cls, update, handler):
        if not handler:
            return
        handler(update.chosen_inline_result.from_.id, update)


class CommandHandler(HandlerPatternMixin):

    @classmethod
    def handle(cls, update, handlers):
        handler = cls.get_handler(update.message.text, handlers)
        handler(update.message.chat.id, update) if handler else None


class ConnectedWebsiteHandler(HandlerSimpleMixin):
    pass


class ContactHandler(HandlerSimpleMixin):
    pass


class DocumentHandler(HandlerSimpleMixin):
    pass


class EditedChannelPostHandler(HandlerSimpleMixin):

    @classmethod
    def handle(cls, update, handler):
        if not handler:
            return
        handler(update.edited_channel_post.chat.id, update)


class EditedMessageHandler(HandlerSimpleMixin):

    @classmethod
    def handle(cls, update, handler):
        if not handler:
            return
        handler(update.edited_message.chat.id, update)


class GameHandler(HandlerSimpleMixin):
    pass


class InlineQueryHandler(HandlerPatternMixin):

    @classmethod
    def handle(cls, update, handlers):
        handler = cls.get_handler(update.inline_query.query, handlers)
        handler(update.inline_query.from_.id, update) if handler else None


class InvoiceHandler(HandlerSimpleMixin):
    pass


class LeftChatMemberHandler(HandlerSimpleMixin):
    pass


class LocationHandler(HandlerSimpleMixin):
    pass


class MessageHandler(HandlerPatternMixin):

    @classmethod
    def handle(cls, update, handlers):
        handler = cls.get_handler(update.message.text, handlers)
        handler(update.message.chat.id, update) if handler else None


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

    @classmethod
    def handle(cls, update, handler):
        if not handler:
            return
        handler(None, update)


class PollAnswerHandler(HandlerSimpleMixin):

    @classmethod
    def handle(cls, update, handler):
        if not handler:
            return
        handler(update.poll_answer.user.id, update)


class PreCheckoutQueryHandler(HandlerSimpleMixin):

    @classmethod
    def handle(cls, update, handler):
        if not handler:
            return
        handler(update.pre_checkout_query.from_.id, update)


class ShippingQueryHandler(HandlerSimpleMixin):

    @classmethod
    def handle(cls, update, handler):
        if not handler:
            return
        handler(update.shipping_query.from_.id, update)


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
