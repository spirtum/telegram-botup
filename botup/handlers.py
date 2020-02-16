class PatternHandler:

    def __init__(self, pattern, function):
        self.pattern = pattern
        self.function = function

    @classmethod
    def get_handler(cls, command, handlers):
        handler = handlers.get(command)
        if not handler:
            for pattern in (c for c in handlers.keys() if hasattr(c, 'match')):
                if pattern.match(command):
                    handler = handlers[pattern]
                    break
        return handler


class SimpleHandler:

    def __init__(self, function):
        self.function = function

    @classmethod
    def handle(cls, update, handler):
        if not handler:
            return
        handler(update.message.chat.id, update)


class AnimationHandler(SimpleHandler):
    pass


class AudioHandler(SimpleHandler):
    pass


class CallbackQueryHandler(PatternHandler):

    @classmethod
    def handle(cls, update, handlers):
        handler = cls.get_handler(update.callback_query.data, handlers)
        handler(update.callback_query.message.chat.id, update) if handler else None


class ChannelPostHandler(SimpleHandler):

    @classmethod
    def handle(cls, update, handler):
        if not handler:
            return
        handler(update.channel_post.chat.id, update)


class ChosenInlineResultHandler(SimpleHandler):

    @classmethod
    def handle(cls, update, handler):
        if not handler:
            return
        handler(update.chosen_inline_result.from_.id, update)


class CommandHandler(PatternHandler):

    @classmethod
    def handle(cls, update, handlers):
        handler = cls.get_handler(update.message.text, handlers)
        handler(update.message.chat.id, update) if handler else None


class ConnectedWebsiteHandler(SimpleHandler):
    pass


class ContactHandler(SimpleHandler):
    pass


class DocumentHandler(SimpleHandler):
    pass


class EditedChannelPostHandler(SimpleHandler):

    @classmethod
    def handle(cls, update, handler):
        if not handler:
            return
        handler(update.edited_channel_post.chat.id, update)


class EditedMessageHandler(SimpleHandler):

    @classmethod
    def handle(cls, update, handler):
        if not handler:
            return
        handler(update.edited_message.chat.id, update)


class GameHandler(SimpleHandler):
    pass


class InlineQueryHandler(PatternHandler):

    @classmethod
    def handle(cls, update, handlers):
        handler = cls.get_handler(update.inline_query.query, handlers)
        handler(update.inline_query.from_.id, update) if handler else None


class InvoiceHandler(SimpleHandler):
    pass


class LeftChatMemberHandler(SimpleHandler):
    pass


class LocationHandler(SimpleHandler):
    pass


class MessageHandler(PatternHandler):

    @classmethod
    def handle(cls, update, handlers):
        handler = cls.get_handler(update.message.text, handlers)
        handler(update.message.chat.id, update) if handler else None


class NewChatMembersHandler(SimpleHandler):
    pass


class NewChatPhotoHandler(SimpleHandler):
    pass


class NewChatTitleHandler(SimpleHandler):
    pass


class PassportDataHandler(SimpleHandler):
    pass


class PhotoHandler(SimpleHandler):
    pass


class PollHandler(SimpleHandler):

    @classmethod
    def handle(cls, update, handler):
        if not handler:
            return
        handler(None, update)


class PollAnswerHandler(SimpleHandler):

    @classmethod
    def handle(cls, update, handler):
        if not handler:
            return
        handler(update.poll_answer.user.id, update)


class PreCheckoutQueryHandler(SimpleHandler):

    @classmethod
    def handle(cls, update, handler):
        if not handler:
            return
        handler(update.pre_checkout_query.from_.id, update)


class ShippingQueryHandler(SimpleHandler):

    @classmethod
    def handle(cls, update, handler):
        if not handler:
            return
        handler(update.shipping_query.from_.id, update)


class StickerHandler(SimpleHandler):
    pass


class SuccessfulPaymentHandler(SimpleHandler):
    pass


class VenueHandler(SimpleHandler):
    pass


class VideoHandler(SimpleHandler):
    pass


class VideoNoteHandler(SimpleHandler):
    pass


class VoiceHandler(SimpleHandler):
    pass
