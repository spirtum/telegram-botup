from .location import Location


class Venue:

    def __init__(self, **kwargs):
        self.location = Location(**kwargs['location'])
        self.title = kwargs.get('title')
        self.address = kwargs.get('address')
        self.foursquare_id = kwargs.get('foursquare_id')
        self.foursquare_type = kwargs.get('foursquare_type')
