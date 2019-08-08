from .inline_query_result import InlineQueryResult


class InlineQueryResultDocument(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'document'
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
        self.document_url = kwargs.get('document_url')
        self.mime_type = kwargs.get('mime_type')
        self.description = kwargs.get('description')
        self.thumb_url = kwargs.get('thumb_url')
        self.thumb_width = kwargs.get('thumb_width')
        self.thumb_height = kwargs.get('thumb_height')
