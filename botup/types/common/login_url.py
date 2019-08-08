class LoginUrl:

    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.forward_text = kwargs.get('forward_text')
        self.bot_username = kwargs.get('bot_username')
        self.request_write_access = kwargs.get('request_write_access')
