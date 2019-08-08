from .inline_query_result import InlineQueryResult


class InlineQueryResultVoice(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'voice'
        self.voice_url = kwargs.get('voice_url')
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
        self.voice_duration = kwargs.get('voice_duration')
