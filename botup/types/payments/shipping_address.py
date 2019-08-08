class ShippingAddress:

    def __init__(self, **kwargs):
        self.country_code = kwargs.get('country_code')
        self.state = kwargs.get('state')
        self.city = kwargs.get('city')
        self.street_line1 = kwargs.get('street_line1')
        self.street_line2 = kwargs.get('street_line2')
        self.post_code = kwargs.get('post_code')
