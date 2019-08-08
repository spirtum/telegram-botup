try:
    import ujson as json
except ImportError:
    import json

from .inline_keyboard_button import InlineKeyboardButton


class InlineKeyboardMarkup:

    def __init__(self, **kwargs):
        self.inline_keyboard = [
            [InlineKeyboardButton(**v) for v in line] for line in kwargs.get('inline_keyboard', [])
        ]

    def line(self, *args):
        self.inline_keyboard.append(args)

    @staticmethod
    def callback_data(text, callback_data):
        return InlineKeyboardButton(text=text, callback_data=callback_data)

    @staticmethod
    def login_url(text, login_url):
        return InlineKeyboardButton(text=text, login_url=login_url)

    @staticmethod
    def switch_inline_query(text, switch_inline_query):
        return InlineKeyboardButton(text=text, switch_inline_query=switch_inline_query)

    @staticmethod
    def switch_inline_query_current_chat(text, switch_inline_query_current_chat):
        return InlineKeyboardButton(text=text, switch_inline_query_current_chat=switch_inline_query_current_chat)

    @staticmethod
    def pay(text, pay=True):
        return InlineKeyboardButton(text=text, pay=pay)

    @staticmethod
    def url(text, url):
        return InlineKeyboardButton(text=text, url=url)

    def clear(self):
        self.inline_keyboard.clear()

    def as_dict(self):
        return json.dumps(dict(inline_keyboard=[[b.as_dict() for b in line] for line in self.inline_keyboard]))
