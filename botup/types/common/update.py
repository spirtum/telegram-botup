from .callback_query import CallbackQuery
from .message import Message
from .poll import Poll
from ..inline_mode.chosen_inline_result import ChosenInlineResult
from ..inline_mode.inline_query import InlineQuery
from ..payments.pre_checkout_query import PreCheckoutQuery
from ..payments.shipping_query import ShippingQuery


class Update:

    def __init__(self, **kwargs):
        self.update_id = kwargs.get('update_id')
        self.message = Message(**kwargs['message']) if 'message' in kwargs else None
        self.edited_message = Message(**kwargs['edited_message']) if 'edited_message' in kwargs else None
        self.channel_post = Message(**kwargs['channel_post']) if 'channel_post' in kwargs else None
        self.edited_channel_post = Message(
            **kwargs['edited__channel_post']) if 'edited__channel_post' in kwargs else None
        self.inline_query = InlineQuery(**kwargs['inline_query']) if 'inline_query' in kwargs else None
        self.chosen_inline_result = ChosenInlineResult(
            **kwargs['chosen_inline_result']) if 'chosen_inline_result' in kwargs else None
        self.callback_query = CallbackQuery(**kwargs['callback_query']) if 'callback_query' in kwargs else None
        self.shipping_query = ShippingQuery(**kwargs['shipping_query']) if 'shipping_query' in kwargs else None
        self.pre_checkout_query = PreCheckoutQuery(
            **kwargs['pre_checkout_query']) if 'pre_checkout_query' in kwargs else None
        self.poll = Poll(**kwargs['poll']) if 'poll' in kwargs else None
