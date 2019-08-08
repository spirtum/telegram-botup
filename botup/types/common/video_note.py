from .photo_size import PhotoSize


class VideoNote:

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.length = kwargs.get('length')
        self.duration = kwargs.get('duration')
        self.thumb = PhotoSize(**kwargs['thumb']) if 'thumb' in kwargs else None
        self.file_size = kwargs.get('file_size')
