from .inline_query_result import InlineQueryResult


class InlineQueryResultArticle(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'article'
        self.title = kwargs.get('title')
        self.url = kwargs.get('url')
        self.hide_url = kwargs.get('hide_url')
        self.description = kwargs.get('description')
        self.thumb_url = kwargs.get('thumb_url')
        self.thumb_width = kwargs.get('thumb_width')
        self.thumb_height = kwargs.get('thumb_height')
