from .base import StringConstant


class StickerType(StringConstant):
    pass


REGULAR = StickerType('regular')
MASK = StickerType('mask')
CUSTOM_EMOJI = StickerType('custom_emoji')
