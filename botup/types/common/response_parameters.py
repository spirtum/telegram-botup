class ResponseParameters:

    def __init__(self, **kwargs):
        self.migrate_to_chat_id = kwargs.get('migrate_to_chat_id')
        self.retry_after = kwargs.get('retry_after')
