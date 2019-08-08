from .login_url import LoginUrl
from ..base_object import BaseObject


class InlineKeyboardButton(BaseObject):
    NESTED_KEYS = ['login_url', ]

    def __init__(self, **kwargs):
        self.text = kwargs.get('text')
        self.url = kwargs.get('url')
        self.login_url = LoginUrl(**kwargs['login_url']) if 'login_url' in kwargs else None
        self.callback_data = kwargs.get('callback_data')
        self.switch_inline_query = kwargs.get('switch_inline_query')
        self.switch_inline_query_current_chat = kwargs.get('switch_inline_query_current_chat')
        self.callback_game = None  # CallbackGame. A placeholder, currently holds no information.
        self.pay = kwargs.get('pay')
