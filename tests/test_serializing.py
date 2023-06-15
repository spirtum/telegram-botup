from botup.types import InlineKeyboardMarkup, InlineKeyboardButton

from tests import utils


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


def test_my_chat_member():
    c = utils.my_chat_member_update()
    assert c


def test_poll():
    c = utils.poll_update()
    assert c.is_poll
