from .labeled_price import LabeledPrice


class ShippingOption:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.title = kwargs.get('title')
        self.prices = [LabeledPrice(**v) for v in kwargs['prices']] if 'prices' in kwargs else None
