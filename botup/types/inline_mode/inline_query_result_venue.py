from .inline_query_result import InlineQueryResult


class InlineQueryResultVenue(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'venue'
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')
        self.title = kwargs.get('title')
        self.address = kwargs.get('address')
        self.foursquare_id = kwargs.get('foursquare_id')
        self.foursquare_type = kwargs.get('foursquare_type')
        self.thumb_url = kwargs.get('thumb_url')
        self.thumb_width = kwargs.get('thumb_width')
        self.thumb_height = kwargs.get('thumb_height')
