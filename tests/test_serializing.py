from botup.types import InlineKeyboardMarkup


def test_inline_keyboard_markup():
    k = InlineKeyboardMarkup()
    k.line(k.callback_data('text1', 'callback1'), k.callback_data('text2', 'callback2'))
    k.line(k.url('text3', 'url'))
    InlineKeyboardMarkup(**k.as_dict())
