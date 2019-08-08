from .inline_query_result import InlineQueryResult


class InlineQueryResultCachedAudio(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'audio'
        self.audio_file_id = kwargs.get('audio_file_id')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
