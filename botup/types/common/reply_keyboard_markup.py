try:
    import ujson as json
except ImportError:
    import json

from .keyboard_button import KeyboardButton


class ReplyKeyboardMarkup:

    def __init__(self, **kwargs):
        self.keyboard = [[KeyboardButton(**v) for v in line] for line in kwargs.get('keyboard', [])]
        self.resize_keyboard = kwargs.get('resize_keyboard')
        self.one_time_keyboard = kwargs.get('one_time_keyboard')
        self.selective = kwargs.get('selective')

    def line(self, *args):
        self.keyboard.append(args)

    @staticmethod
    def button(text, request_contact=False, request_location=False):
        return KeyboardButton(text=text, request_contact=request_contact, request_location=request_location)

    def as_dict(self):
        result = {k: v for k, v in vars(self).items() if v is not None}
        result['keyboard'] = [[b.as_dict() for b in line] for line in self.keyboard]
        return json.dumps(result)
