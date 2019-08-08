from .inline_query_result import InlineQueryResult


class InlineQueryResultLocation(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'location'
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')
        self.title = kwargs.get('title')
        self.live_period = kwargs.get('live_period')
        self.thumb_url = kwargs.get('thumb_url')
        self.thumb_width = kwargs.get('thumb_width')
        self.thumb_height = kwargs.get('thumb_height')
