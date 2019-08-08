from .input_message_content import InputMessageContent


class InputTextMessageContent(InputMessageContent):

    def __init__(self, **kwargs):
        self.message_text = kwargs.get('message_text')
        self.parse_mode = kwargs.get('parse_mode')
        self.disable_web_page_preview = kwargs.get('disable_web_page_preview')
