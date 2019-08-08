class BaseElementError:

    def __init__(self, **kwargs):
        self.source = kwargs.get('source')
        self.type = kwargs.get('type')
        self.message = kwargs.get('message')
