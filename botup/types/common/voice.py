class Voice:

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.duration = kwargs.get('duration')
        self.mime_type = kwargs.get('mime_type')
        self.file_size = kwargs.get('file_size')
