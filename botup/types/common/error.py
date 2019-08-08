class ErrorResponse:

    def __init__(self, **kwargs):
        self.raw_data = kwargs
        self.ok = kwargs.get('ok')
        self.error_code = kwargs.get('error_code')
        self.description = kwargs.get('description')
