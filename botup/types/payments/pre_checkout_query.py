from .order_info import OrderInfo
from ..common.user import User


class PreCheckoutQuery:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.from_ = User(**kwargs['from']) if 'from' in kwargs else None
        self.currency = kwargs.get('currency')
        self.total_amount = kwargs.get('total_amount')
        self.invoice_payload = kwargs.get('invoice_payload')
        self.shipping_option_id = kwargs.get('shipping_option_id')
        self.order_info = OrderInfo(**kwargs['order_info']) if 'order_info' in kwargs else None
