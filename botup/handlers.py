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
    async def handle(cls, update, handler):
        if not handler:
            return
        await handler(update.message.chat.id, update)
        return True


class AnimationHandler(SimpleHandler):
    pass


class AudioHandler(SimpleHandler):
    pass


class CallbackQueryHandler(PatternHandler):

    @classmethod
    async def handle(cls, update, handlers):
        handler = cls.get_handler(update.callback_query.data, handlers)
        if handler:
            await handler(update.callback_query.message.chat.id, update)
            return True


class ChannelPostHandler(SimpleHandler):

    @classmethod
    async def handle(cls, update, handler):
        if not handler:
            return
        await handler(update.channel_post.chat.id, update)
        return True


class ChosenInlineResultHandler(SimpleHandler):

    @classmethod
    async def handle(cls, update, handler):
        if not handler:
            return
        await handler(update.chosen_inline_result.from_.id, update)
        return True


class CommandHandler(PatternHandler):

    @classmethod
    async def handle(cls, update, handlers):
        handler = cls.get_handler(update.message.text, handlers)
        if handler:
            await handler(update.message.chat.id, update)
            return True


class ConnectedWebsiteHandler(SimpleHandler):
    pass


class ContactHandler(SimpleHandler):
    pass


class DiceHandler(SimpleHandler):
    pass


class DocumentHandler(SimpleHandler):
    pass


class EditedChannelPostHandler(SimpleHandler):

    @classmethod
    async def handle(cls, update, handler):
        if not handler:
            return
        await handler(update.edited_channel_post.chat.id, update)
        return True


class EditedMessageHandler(SimpleHandler):

    @classmethod
    async def handle(cls, update, handler):
        if not handler:
            return
        await handler(update.edited_message.chat.id, update)
        return True


class GameHandler(SimpleHandler):
    pass


class InlineQueryHandler(PatternHandler):

    @classmethod
    async def handle(cls, update, handlers):
        handler = cls.get_handler(update.inline_query.query, handlers)
        if handler:
            await handler(update.inline_query.from_.id, update)
            return True


class InvoiceHandler(SimpleHandler):
    pass


class LeftChatMemberHandler(SimpleHandler):
    pass


class LocationHandler(SimpleHandler):
    pass


class MessageHandler(PatternHandler):

    @classmethod
    async def handle(cls, update, handlers):
        handler = cls.get_handler(update.message.text, handlers)
        if handler:
            await handler(update.message.chat.id, update)
            return True


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
    async def handle(cls, update, handler):
        if not handler:
            return
        await handler(None, update)
        return True


class PollAnswerHandler(SimpleHandler):

    @classmethod
    async def handle(cls, update, handler):
        if not handler:
            return
        await handler(update.poll_answer.user.id, update)
        return True


class PreCheckoutQueryHandler(SimpleHandler):

    @classmethod
    async def handle(cls, update, handler):
        if not handler:
            return
        await handler(update.pre_checkout_query.from_.id, update)
        return True


class ShippingQueryHandler(SimpleHandler):

    @classmethod
    async def handle(cls, update, handler):
        if not handler:
            return
        await handler(update.shipping_query.from_.id, update)
        return True


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
