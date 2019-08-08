class ShippingQueryHandler:

    def __init__(self, update, user_handler):
        self.update = update
        self.user_handler = user_handler

    def handle(self):
        if not self.user_handler:
            return
        self.user_handler(chat_id=self.update.shipping_query.from_.id, update=self.update)
