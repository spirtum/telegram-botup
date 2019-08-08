class LabeledPrice:

    def __init__(self, **kwargs):
        self.label = kwargs.get('label')
        self.amount = kwargs.get('amount')
