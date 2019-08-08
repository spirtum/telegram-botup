import threading

try:
    import ujson as json
except ImportError:
    import json

from .types.common import Update
from .handlers import (
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    ChannelPostHandler,
    ChosenInlineResultHandler,
    EditedChannelPostHandler,
    EditedMessageHandler,
    PollHandler,
    PreCheckoutQueryHandler,
    ShippingQueryHandler
)


class Bot:

    def __init__(self):
        self._commands = dict()
        self._callbacks = dict()
        self._messages = dict()
        self._inlines = dict()
        self._channel_post_handler = None
        self._chosen_inline_result_handler = None
        self._edited_channel_post_handler = None
        self._edited_message_handler = None
        self._poll_handler = None
        self._pre_checkout_query_handler = None
        self._shipping_query_handler = None

    def register_command_handler(self, command, handler):
        if not command.startswith('/'):
            command = f'/{command}'
        self._commands[command] = handler

    def register_message_handler(self, message, handler):
        self._messages[message] = handler

    def register_callback_handler(self, callback, handler):
        self._callbacks[callback] = handler

    def register_inline_handler(self, inline_query, handler):
        self._inlines[inline_query] = handler

    def register_channel_post_handler(self, handler):
        self._channel_post_handler = handler

    def register_edited_message_handler(self, handler):
        self._edited_message_handler = handler

    def register_edited_channel_post_handler(self, handler):
        self._edited_channel_post_handler = handler

    def register_chosen_inline_result_handler(self, handler):
        self._chosen_inline_result_handler = handler

    def register_shipping_query_handler(self, handler):
        self._shipping_query_handler = handler

    def register_pre_checkout_query_handler(self, handler):
        self._pre_checkout_query_handler = handler

    def register_poll_handler(self, handler):
        self._poll_handler = handler

    def handle(self, request):
        if 'update_id' not in request:
            return
        update = Update(**request)
        keyword_arguments = dict(update=update)
        if update.callback_query:
            keyword_arguments['user_handlers'] = self._callbacks
            handler = CallbackQueryHandler(**keyword_arguments)
        elif update.message:
            if not update.message.text:
                return
            keyword_arguments['user_handlers'] = self._messages
            handler = MessageHandler(**keyword_arguments)
            if update.message.text.startswith('/'):
                keyword_arguments['user_handlers'] = self._commands
                handler = CommandHandler(**keyword_arguments)
        elif update.inline_query:
            keyword_arguments['user_handlers'] = self._inlines
            handler = InlineQueryHandler(**keyword_arguments)
        elif update.edited_message:
            keyword_arguments['user_handler'] = self._edited_message_handler
            handler = EditedMessageHandler(**keyword_arguments)
        elif update.channel_post:
            keyword_arguments['user_handler'] = self._channel_post_handler
            handler = ChannelPostHandler(**keyword_arguments)
        elif update.edited_channel_post:
            keyword_arguments['user_handler'] = self._edited_channel_post_handler
            handler = EditedChannelPostHandler(**keyword_arguments)
        elif update.chosen_inline_result:
            keyword_arguments['user_handler'] = self._chosen_inline_result_handler
            handler = ChosenInlineResultHandler(**keyword_arguments)
        elif update.shipping_query:
            keyword_arguments['user_handler'] = self._shipping_query_handler
            handler = ShippingQueryHandler(**keyword_arguments)
        elif update.pre_checkout_query:
            keyword_arguments['user_handler'] = self._pre_checkout_query_handler
            handler = PreCheckoutQueryHandler(**keyword_arguments)
        elif update.poll:
            keyword_arguments['user_handler'] = self._poll_handler
            handler = PollHandler(**keyword_arguments)
        else:
            return
        handler.handle()

    def polling(self, form, tick=1.0, limit=None, timeout=None, allowed_updates=None):
        from .form import Form
        assert isinstance(form, Form), 'Wrong type of form. Must be a botup.form.Form'
        last_update_id = 0
        response = form.get_updates(limit=limit, timeout=timeout, allowed_updates=allowed_updates)
        while True:
            response = json.loads(response)
            for update in response['result']:
                last_update_id = update['update_id']
                self.handle(update)
            timer = threading.Timer(tick, lambda *args: None)
            timer.start()
            timer.join()
            response = form.get_updates(
                offset=last_update_id + 1,
                limit=limit,
                timeout=timeout,
                allowed_updates=allowed_updates
            )
