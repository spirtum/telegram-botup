import asyncio

from tests import utils


def test_middleware(dispatcher):
    update = utils.message_update_by_text('test')
    calls = list()

    @dispatcher.middleware
    async def mw_first(u):
        calls.append(mw_first)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is mw_first


def test_command_handler(dispatcher):
    a_command_update = utils.command_update_by_text('/a')
    b_command_update = utils.command_update_by_text('/b')

    contexts = list()
    calls = list()

    @dispatcher.command_handler('/a')
    async def a_handler(u):
        contexts.append(u)
        calls.append(a_handler)

    asyncio.run(dispatcher.handle_context(b_command_update))
    assert not calls
    asyncio.run(dispatcher.handle_context(a_command_update))
    assert calls[-1] is a_handler
    assert contexts[-1] is a_command_update


def test_callback_handler(dispatcher):
    a_callback_update = utils.callback_update_by_data('a')
    b_callback_update = utils.callback_update_by_data('b')

    contexts = list()
    calls = list()

    @dispatcher.callback_handler('a')
    async def a_callback_handler(u):
        contexts.append(u)
        calls.append(a_callback_handler)

    asyncio.run(dispatcher.handle_context(b_callback_update))
    assert not calls
    asyncio.run(dispatcher.handle_context(a_callback_update))
    assert calls[-1] is a_callback_handler
    assert contexts[-1] is a_callback_update


def test_message_handler(dispatcher):
    a_message_update = utils.message_update_by_text('a')
    b_message_update = utils.message_update_by_text('b')

    contexts = list()
    calls = list()

    @dispatcher.message_handler('a')
    async def a_message_handler(u):
        contexts.append(u)
        calls.append(a_message_handler)

    asyncio.run(dispatcher.handle_context(b_message_update))
    assert not calls
    asyncio.run(dispatcher.handle_context(a_message_update))
    assert calls[-1] is a_message_handler
    assert contexts[-1] is a_message_update


def test_inline_handler(dispatcher):
    a_inline_update = utils.inline_query_update_by_query('a')
    b_inline_update = utils.inline_query_update_by_query('b')

    contexts = list()
    calls = list()

    @dispatcher.inline_handler('a')
    async def a_inline_handler(u):
        contexts.append(u)
        calls.append(a_inline_handler)

    asyncio.run(dispatcher.handle_context(b_inline_update))
    assert not calls
    asyncio.run(dispatcher.handle_context(a_inline_update))
    assert calls[-1] is a_inline_handler
    assert contexts[-1] is a_inline_update


def test_channel_post_handler(dispatcher):
    channel_post_update = utils.channel_post_update()

    contexts = list()
    calls = list()

    @dispatcher.channel_post_handler
    async def channel_post_handler(u):
        contexts.append(u)
        calls.append(channel_post_handler)

    asyncio.run(dispatcher.handle_context(channel_post_update))
    assert calls[-1] is channel_post_handler
    assert contexts[-1] is channel_post_update


def test_chosen_inline_result_handler(dispatcher):
    update = utils.chosen_inline_result_update()

    contexts = list()
    calls = list()

    @dispatcher.chosen_inline_result_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_edited_channel_post_handler(dispatcher):
    update = utils.edited_channel_post_update()

    contexts = list()
    calls = list()

    @dispatcher.edited_channel_post_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_edited_message_handler(dispatcher):
    update = utils.edited_message_update_by_text('message')

    contexts = list()
    calls = list()

    @dispatcher.edited_message_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_poll_handler(dispatcher):
    update = utils.poll_update()

    contexts = list()
    calls = list()

    @dispatcher.poll_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_poll_answer_handler(dispatcher):
    update = utils.poll_answer_update()

    contexts = list()
    calls = list()

    @dispatcher.poll_answer_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_dice_handler(dispatcher):
    update = utils.dice_update()

    contexts = list()
    calls = list()

    @dispatcher.dice_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_document_handler(dispatcher):
    update = utils.document_update()

    contexts = list()
    calls = list()

    @dispatcher.document_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_animation_handler(dispatcher):
    update = utils.animation_update()

    contexts = list()
    calls = list()

    @dispatcher.animation_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_audio_handler(dispatcher):
    update = utils.audio_update()

    contexts = list()
    calls = list()

    @dispatcher.audio_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_contact_handler(dispatcher):
    update = utils.contact_update()

    contexts = list()
    calls = list()

    @dispatcher.contact_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_left_chat_member_handler(dispatcher):
    update = utils.left_chat_member_update()

    contexts = list()
    calls = list()

    @dispatcher.left_chat_member_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_location_handler(dispatcher):
    update = utils.location_update()

    contexts = list()
    calls = list()

    @dispatcher.location_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_new_chat_members_handler(dispatcher):
    update = utils.new_chat_members_update()

    contexts = list()
    calls = list()

    @dispatcher.new_chat_members_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_new_chat_photo_handler(dispatcher):
    update = utils.new_chat_photo_update()

    contexts = list()
    calls = list()

    @dispatcher.new_chat_photo_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_new_chat_title_handler(dispatcher):
    update = utils.new_chat_title_update()

    contexts = list()
    calls = list()

    @dispatcher.new_chat_title_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_photo_handler(dispatcher):
    update = utils.photo_update()

    contexts = list()
    calls = list()

    @dispatcher.photo_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_sticker_handler(dispatcher):
    update = utils.sticker_update()

    contexts = list()
    calls = list()

    @dispatcher.sticker_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_venue_handler(dispatcher):
    update = utils.venue_update()

    contexts = list()
    calls = list()

    @dispatcher.venue_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_video_handler(dispatcher):
    update = utils.video_update()

    contexts = list()
    calls = list()

    @dispatcher.video_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_video_note_handler(dispatcher):
    update = utils.video_note_update()

    contexts = list()
    calls = list()

    @dispatcher.video_note_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


def test_voice_handler(dispatcher):
    update = utils.voice_update()

    contexts = list()
    calls = list()

    @dispatcher.voice_handler
    async def handler(u):
        contexts.append(u)
        calls.append(handler)

    asyncio.run(dispatcher.handle_context(update))
    assert calls[-1] is handler
    assert contexts[-1] is update


# TODO test_pre_checkout_query_handler
# TODO test_shipping_query_handler
# TODO test_connected_website_handler
# TODO test_game_handler
# TODO test_invoice_handler
# TODO test_passport_data_handler
# TODO test_successful_payment_handler
