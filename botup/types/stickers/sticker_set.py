from .sticker import Sticker


class StickerSet:

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.title = kwargs.get('title')
        self.contains_masks = kwargs.get('contains_masks')
        self.stickers = [Sticker(**v) for v in kwargs['stickers']] if 'stickers' in kwargs else []
