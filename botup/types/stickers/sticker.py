from .mask_position import MaskPosition
from ..common.photo_size import PhotoSize


class Sticker:

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.thumb = PhotoSize(**kwargs['thumb']) if 'thumb' in kwargs else None
        self.emoji = kwargs.get('emoji')
        self.set_name = kwargs.get('set_name')
        self.mask_position = MaskPosition(**kwargs['mask_position']) if 'mask_position' in kwargs else None
        self.file_size = kwargs.get('file_size')
