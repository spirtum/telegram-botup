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
        self._statements = set()
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
        self._statements.add(self._is_command)
        if not command.startswith('/'):
            command = f'/{command}'
        self._commands[command] = handler

    def register_message_handler(self, message, handler):
        self._statements.add(self._is_message)
        self._messages[message] = handler

    def register_callback_handler(self, callback, handler):
        self._statements.add(self._is_callback)
        self._callbacks[callback] = handler

    def register_inline_handler(self, inline_query, handler):
        self._statements.add(self._is_inline)
        self._inlines[inline_query] = handler

    def register_channel_post_handler(self, handler):
        self._statements.add(self._is_channel_post)
        self._channel_post_handler = handler

    def register_edited_message_handler(self, handler):
        self._statements.add(self._is_edited_message)
        self._edited_message_handler = handler

    def register_edited_channel_post_handler(self, handler):
        self._statements.add(self._is_edited_channel_post)
        self._edited_channel_post_handler = handler

    def register_chosen_inline_result_handler(self, handler):
        self._statements.add(self._is_chosen_inline_result)
        self._chosen_inline_result_handler = handler

    def register_shipping_query_handler(self, handler):
        self._statements.add(self._is_shipping_query)
        self._shipping_query_handler = handler

    def register_pre_checkout_query_handler(self, handler):
        self._statements.add(self._is_pre_checkout_query)
        self._pre_checkout_query_handler = handler

    def register_poll_handler(self, handler):
        self._statements.add(self._is_poll)
        self._poll_handler = handler

    def _is_command(self, update):
        if update.message and update.message.text and update.message.text.startswith('/'):
            CommandHandler(update=update, user_handlers=self._commands).handle()

    def _is_message(self, update):
        if update.message and update.message.text and not update.message.text.startswith('/'):
            MessageHandler(update=update, user_handlers=self._messages).handle()

    def _is_callback(self, update):
        if update.callback_query:
            CallbackQueryHandler(update=update, user_handlers=self._callbacks).handle()

    def _is_inline(self, update):
        if update.inline_query:
            InlineQueryHandler(update=update, user_handlers=self._inlines).handle()

    def _is_channel_post(self, update):
        if update.channel_post:
            ChannelPostHandler(update=update, user_handler=self._channel_post_handler).handle()

    def _is_edited_message(self, update):
        if update.edited_message:
            EditedMessageHandler(update=update, user_handler=self._edited_message_handler).handle()

    def _is_edited_channel_post(self, update):
        if update.edited_channel_post:
            EditedChannelPostHandler(update=update, user_handler=self._edited_channel_post_handler).handle()

    def _is_chosen_inline_result(self, update):
        if update.chosen_inline_result:
            ChosenInlineResultHandler(update=update, user_handler=self._chosen_inline_result_handler).handle()

    def _is_shipping_query(self, update):
        if update.shipping_query:
            ShippingQueryHandler(update=update, user_handler=self._shipping_query_handler).handle()

    def _is_pre_checkout_query(self, update):
        if update.pre_checkout_query:
            PreCheckoutQueryHandler(update=update, user_handler=self._pre_checkout_query_handler).handle()

    def _is_poll(self, update):
        if update.poll:
            PollHandler(update=update, user_handler=self._poll_handler).handle()

    def handle(self, request):
        if 'update_id' not in request:
            return
        update = Update(**request)
        for statement in self._statements:
            statement(update)

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
