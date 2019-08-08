from .photo_size import PhotoSize


class UserProfilePhotos:

    def __init__(self, **kwargs):
        self.total_count = kwargs.get('total_count')
        self.photos = [PhotoSize(**v) for v in kwargs['photos']] if 'photos' in kwargs else []
