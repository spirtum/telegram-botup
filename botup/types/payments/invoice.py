class Invoice:

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.start_parameter = kwargs.get('start_parameter')
        self.currency = kwargs.get('currency')
        self.total_amount = kwargs.get('total_amount')
