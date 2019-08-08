from .photo_size import PhotoSize


class Audio:

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.duration = kwargs.get('duration')
        self.performer = kwargs.get('performer')
        self.title = kwargs.get('title')
        self.mime_type = kwargs.get('mime_type')
        self.file_size = kwargs.get('file_size')
        self.thumb = PhotoSize(**kwargs['thumb']) if 'thumb' in kwargs else None
