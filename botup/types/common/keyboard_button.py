from ..base_object import BaseObject


class KeyboardButton(BaseObject):

    def __init__(self, **kwargs):
        self.text = kwargs.get('text')
        self.request_contact = kwargs.get('request_contact')
        self.request_location = kwargs.get('request_location')
