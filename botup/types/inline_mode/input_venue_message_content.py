from .input_message_content import InputMessageContent


class InputVenueMessageContent(InputMessageContent):

    def __init__(self, **kwargs):
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')
        self.title = kwargs.get('title')
        self.address = kwargs.get('address')
        self.foursquare_id = kwargs.get('foursquare_id')
        self.foursquare_type = kwargs.get('foursquare_type')
