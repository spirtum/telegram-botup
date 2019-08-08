from .inline_query_result import InlineQueryResult


class InlineQueryResultCachedGif(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'gif'
        self.gif_file_id = kwargs.get('gif_file_id')
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
