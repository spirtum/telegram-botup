from .inline_query_result import InlineQueryResult


class InlineQueryResultCachedDocument(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'document'
        self.title = kwargs.get('title')
        self.document_file_id = kwargs.get('document_file_id')
        self.description = kwargs.get('description')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
