from .shipping_address import ShippingAddress
from ..common.user import User


class ShippingQuery:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.from_ = User(**kwargs['from']) if 'from' in kwargs else None
        self.invoice_payload = kwargs.get('invoice_payload')
        self.shipping_address = ShippingAddress(**kwargs['shipping_address']) if 'shipping_address' in kwargs else None
