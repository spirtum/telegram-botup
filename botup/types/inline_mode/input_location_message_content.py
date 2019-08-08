from .input_message_content import InputMessageContent


class InputLocationMessageContent(InputMessageContent):

    def __init__(self, **kwargs):
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')
        self.live_period = kwargs.get('live_period')
