from .inline_query_result import InlineQueryResult


class InlineQueryResultCachedPhoto(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'photo'
        self.photo_file_id = kwargs.get('photo_file_id')
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
