class WebhookInfo:

    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.has_custom_certificate = kwargs.get('has_custom_certificate')
        self.pending_update_count = kwargs.get('pending_update_count')
        self.last_error_date = kwargs.get('last_error_date')
        self.last_error_message = kwargs.get('last_error_message')
        self.max_connections = kwargs.get('max_connections')
        self.allowed_updates = kwargs.get('allowed_updates', list())
