try:
    import ujson as json
except ImportError:
    import json


class ReplyKeyboardRemove:

    def __init__(self, **kwargs):
        self.remove_keyboard = True
        self.selective = kwargs.get('selective')

    def as_dict(self):
        result = {k: v for k, v in vars(self).items() if v is not None}
        return json.dumps(result)
