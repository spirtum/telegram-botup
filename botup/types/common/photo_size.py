class PhotoSize:

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.file_size = kwargs.get('file_size')
