class Location:

    def __init__(self, **kwargs):
        self.longitude = kwargs.get('longitude')
        self.latitude = kwargs.get('latitude')
