from .mixins import PatternMixin


class CallbackQueryHandler(PatternMixin):

    def __init__(self, update, user_handlers):
        self.update = update
        self.handlers = user_handlers

    def handle(self):
        handler = self.get_handler(self.update.callback_query.data)
        handler(chat_id=self.update.callback_query.message.chat.id, update=self.update) if handler else None
