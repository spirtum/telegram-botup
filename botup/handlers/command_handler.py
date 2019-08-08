from .mixins import PatternMixin


class CommandHandler(PatternMixin):

    def __init__(self, update, user_handlers):
        self.update = update
        self.handlers = user_handlers

    def handle(self):
        handler = self.get_handler(self.update.message.text)
        handler(chat_id=self.update.message.chat.id, update=self.update) if handler else None
