from .inline_query_result import InlineQueryResult


class InlineQueryResultCachedVoice(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'voice'
        self.voice_file_id = kwargs.get('voice_file_id')
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
