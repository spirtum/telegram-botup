from .inline_query_result import InlineQueryResult


class InlineQueryResultCachedMpeg4Gif(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'mpeg4_gif'
        self.mpeg4_file_id = kwargs.get('mpeg4_file_id')
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
