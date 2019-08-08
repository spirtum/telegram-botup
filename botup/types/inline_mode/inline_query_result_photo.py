from .inline_query_result import InlineQueryResult


class InlineQueryResultPhoto(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'photo'
        self.photo_url = kwargs.get('photo_url')
        self.thumb_url = kwargs.get('thumb_url')
        self.photo_width = kwargs.get('thumb_width')
        self.photo_height = kwargs.get('thumb_height')
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
