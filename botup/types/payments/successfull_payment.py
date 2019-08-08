from .order_info import OrderInfo


class SuccessfulPayment:

    def __init__(self, **kwargs):
        self.currency = kwargs.get('currency')
        self.total_amount = kwargs.get('total_amount')
        self.invoice_payload = kwargs.get('invoice_payload')
        self.shipping_option_id = kwargs.get('shipping_option_id')
        self.order_info = OrderInfo(**kwargs['order_info']) if 'order_info' in kwargs else None
        self.telegram_payment_charge_id = kwargs.get('telegram_payment_charge_id')
        self.provider_payment_charge_id = kwargs.get('provider_payment_charge_id')
