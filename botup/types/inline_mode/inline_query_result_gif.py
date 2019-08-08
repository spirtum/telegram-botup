from .inline_query_result import InlineQueryResult


class InlineQueryResultGif(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'gif'
        self.gif_url = kwargs.get('gif_url')
        self.gif_width = kwargs.get('gif_width')
        self.gif_height = kwargs.get('gif_height')
        self.gif_duration = kwargs.get('gif_duration')
        self.thumb_url = kwargs.get('thumb_url')
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
