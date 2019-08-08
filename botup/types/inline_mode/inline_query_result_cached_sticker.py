from .inline_query_result import InlineQueryResult


class InlineQueryResultCachedSticker(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'sticker'
        self.sticker_file_id = kwargs.get('sticker_file_id')
