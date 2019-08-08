from .inline_query_result import InlineQueryResult


class InlineQueryResultAudio(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'audio'
        self.audio_url = kwargs.get('audio_url')
        self.parse_mode = kwargs.get('parse_mode')
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.performer = kwargs.get('performer')
        self.audio_duration = kwargs.get('audio_duration')
