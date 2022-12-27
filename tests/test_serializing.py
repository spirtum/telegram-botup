from botup.core.types import InlineKeyboardMarkup, InlineKeyboardButton


def test_inline_keyboard_markup():
    k = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton('text1', callback_data='callback1'),
             InlineKeyboardButton('text2', callback_data='callback2')],
            [
                InlineKeyboardButton('text3', url='url')
            ]
        ]
    )
    InlineKeyboardMarkup.from_dict(k.as_dict())
