from .mixins import PatternMixin


class InlineQueryHandler(PatternMixin):

    def __init__(self, update, user_handlers):
        self.update = update
        self.handlers = user_handlers

    def handle(self):
        handler = self.get_handler(self.update.inline_query.query)
        handler(chat_id=self.update.inline_query.from_.id, update=self.update) if handler else None
