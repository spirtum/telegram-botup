from .inline_query_result import InlineQueryResult


class InlineQueryResultMpeg4Gif(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'mpeg4_gif'
        self.mpeg4_url = kwargs.get('mpeg4_url')
        self.mpeg4_width = kwargs.get('mpeg4_width')
        self.mpeg4_height = kwargs.get('mpeg4_height')
        self.mpeg4_duration = kwargs.get('mpeg4_duration')
        self.thumb_url = kwargs.get('thumb_url')
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
