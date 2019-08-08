from .shipping_address import ShippingAddress


class OrderInfo:

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.phone_number = kwargs.get('phone_number')
        self.email = kwargs.get('email')
        self.shipping_address = ShippingAddress(**kwargs['shipping_address']) if 'shipping_address' in kwargs else None
