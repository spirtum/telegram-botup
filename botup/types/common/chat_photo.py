class ChatPhoto:

    def __init__(self, **kwargs):
        self.small_file_id = kwargs.get('small_file_id')
        self.big_file_id = kwargs.get('big_file_id')
