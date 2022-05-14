import re
import asyncio

from tests import utils


def test_patterns_regexp(dispatcher):
    foobar_message_update = utils.message_update_by_text('foobar')
    hi_dude_message_update = utils.message_update_by_text('hi dude')
    hi_mate_message_update = utils.message_update_by_text('hi mate')
    foobar_callback_update = utils.callback_update_by_data('foobar')
    drop_a_callback_update = utils.callback_update_by_data('drop_a')
    drop_b_callback_update = utils.callback_update_by_data('drop_b')
    foobar_command_update = utils.command_update_by_text('/foobar')
    give_1_command_update = utils.command_update_by_text('/give_1')
    give_2_command_update = utils.command_update_by_text('/give_2')
    foobar_inline_query_update = utils.inline_query_update_by_query('foobar')
    send_a_inline_query_update = utils.inline_query_update_by_query('send a')
    send_b_inline_query_update = utils.inline_query_update_by_query('send b')

    calls = list()
    updates = list()

    async def hi_message_handler(c, u):
        updates.append(u)
        calls.append(hi_message_handler)

    async def drop_callback_handler(c, u):
        updates.append(u)
        calls.append(drop_callback_handler)

    async def give_command_handler(c, u):
        updates.append(u)
        calls.append(give_command_handler)

    async def send_inline_query_handler(c, u):
        updates.append(u)
        calls.append(send_inline_query_handler)

    async def common_handler(c, u):
        updates.append(u)
        calls.append(common_handler)

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(hi_dude_message_update))
    asyncio.run(dispatcher.handle(hi_mate_message_update))
    asyncio.run(dispatcher.handle(foobar_message_update))
    assert before_calls_counter == len(calls)
    dispatcher.register_message_handler(re.compile('^hi'), hi_message_handler)
    asyncio.run(dispatcher.handle(hi_dude_message_update))
    assert calls[-1] is hi_message_handler
    assert updates[-1] is hi_dude_message_update
    asyncio.run(dispatcher.handle(hi_mate_message_update))
    assert calls[-1] is hi_message_handler
    assert updates[-1] is hi_mate_message_update
    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(foobar_message_update))
    assert before_calls_counter == len(calls)
    dispatcher.register_message_handler(re.compile('.*'), common_handler)
    asyncio.run(dispatcher.handle(foobar_message_update))
    assert calls[-1] is common_handler
    assert updates[-1] is foobar_message_update

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(drop_a_callback_update))
    asyncio.run(dispatcher.handle(drop_b_callback_update))
    asyncio.run(dispatcher.handle(foobar_callback_update))
    assert before_calls_counter == len(calls)
    dispatcher.register_callback_handler(re.compile('^drop'), drop_callback_handler)
    asyncio.run(dispatcher.handle(drop_a_callback_update))
    assert calls[-1] is drop_callback_handler
    assert updates[-1] is drop_a_callback_update
    asyncio.run(dispatcher.handle(drop_b_callback_update))
    assert calls[-1] is drop_callback_handler
    assert updates[-1] is drop_b_callback_update
    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(foobar_callback_update))
    assert before_calls_counter == len(calls)
    dispatcher.register_callback_handler(re.compile('.*'), common_handler)
    asyncio.run(dispatcher.handle(foobar_callback_update))
    assert calls[-1] is common_handler
    assert updates[-1] is foobar_callback_update

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(give_1_command_update))
    asyncio.run(dispatcher.handle(give_2_command_update))
    asyncio.run(dispatcher.handle(foobar_command_update))
    assert before_calls_counter == len(calls)
    dispatcher.register_command_handler(re.compile('^/give'), give_command_handler)
    asyncio.run(dispatcher.handle(give_1_command_update))
    assert calls[-1] is give_command_handler
    assert updates[-1] is give_1_command_update
    asyncio.run(dispatcher.handle(give_2_command_update))
    assert calls[-1] is give_command_handler
    assert updates[-1] is give_2_command_update
    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(foobar_command_update))
    assert before_calls_counter == len(calls)
    dispatcher.register_command_handler(re.compile('^/.*'), common_handler)
    asyncio.run(dispatcher.handle(foobar_command_update))
    assert calls[-1] is common_handler
    assert updates[-1] is foobar_command_update
    
    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(send_a_inline_query_update))
    asyncio.run(dispatcher.handle(send_b_inline_query_update))
    asyncio.run(dispatcher.handle(foobar_inline_query_update))
    assert before_calls_counter == len(calls)
    dispatcher.register_inline_handler(re.compile('^send'), send_inline_query_handler)
    asyncio.run(dispatcher.handle(send_a_inline_query_update))
    assert calls[-1] is send_inline_query_handler
    assert updates[-1] is send_a_inline_query_update
    asyncio.run(dispatcher.handle(send_b_inline_query_update))
    assert calls[-1] is send_inline_query_handler
    assert updates[-1] is send_b_inline_query_update
    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(foobar_inline_query_update))
    assert before_calls_counter == len(calls)
    dispatcher.register_inline_handler(re.compile('.*'), common_handler)
    asyncio.run(dispatcher.handle(foobar_inline_query_update))
    assert calls[-1] is common_handler
    assert updates[-1] is foobar_inline_query_update


def test_middleware(dispatcher):
    update = utils.message_update_by_text('test')
    calls = list()

    async def mw_true(u):
        calls.append(mw_true)
        return True

    async def mw_false(u):
        calls.append(mw_false)
        return False

    async def message_handler(c, u):
        calls.append(message_handler)

    asyncio.run(dispatcher.handle(update))
    assert not calls
    dispatcher.register_message_handler('test', message_handler)
    asyncio.run(dispatcher.handle(update))
    assert len(calls) == 1
    assert calls[-1] is message_handler
    dispatcher.register_middleware(mw_false)
    asyncio.run(dispatcher.handle(update))
    assert len(calls) == 3
    assert calls[-2] is mw_false
    assert calls[-1] is message_handler
    dispatcher.register_middleware(mw_true)
    asyncio.run(dispatcher.handle(update))
    assert len(calls) == 5
    assert calls[-2] is mw_false
    assert calls[-1] is mw_true


def test_messages(dispatcher):
    a_messsage_update = utils.message_update_by_text('a')
    b_message_update = utils.message_update_by_text('b')
    c_message_update = utils.message_update_by_text('c')
    command_update = utils.command_update_by_text('/command')

    calls = list()
    updates = list()

    async def a_handler(c, u):
        updates.append(u)
        calls.append(a_handler)

    async def b_handler(c, u):
        updates.append(u)
        calls.append(b_handler)

    async def c_handler(c, u):
        updates.append(u)
        calls.append(c_handler)

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(a_messsage_update))
    asyncio.run(dispatcher.handle(b_message_update))
    asyncio.run(dispatcher.handle(c_message_update))
    assert before_calls_counter == len(calls)

    dispatcher.register_message_handler('a', a_handler)
    dispatcher.register_message_handler('b', b_handler)

    asyncio.run(dispatcher.handle(a_messsage_update))
    assert calls[-1] is a_handler
    assert updates[-1] is a_messsage_update

    asyncio.run(dispatcher.handle(b_message_update))
    assert calls[-1] is b_handler
    assert updates[-1] is b_message_update

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(command_update))
    assert before_calls_counter == len(calls)

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(c_message_update))
    assert before_calls_counter == len(calls)

    dispatcher.register_message_handler('c', c_handler)
    asyncio.run(dispatcher.handle(c_message_update))
    assert calls[-1] is c_handler
    assert updates[-1] is c_message_update


def test_commands(dispatcher):
    a_command_update = utils.command_update_by_text('/a')
    b_command_update = utils.command_update_by_text('/b')
    c_command_update = utils.command_update_by_text('/c')
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def a_handler(c, u):
        updates.append(u)
        calls.append(a_handler)

    async def b_handler(c, u):
        updates.append(u)
        calls.append(b_handler)

    async def c_handler(c, u):
        updates.append(u)
        calls.append(c_handler)

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(a_command_update))
    asyncio.run(dispatcher.handle(b_command_update))
    asyncio.run(dispatcher.handle(c_command_update))
    assert before_calls_counter == len(calls)

    dispatcher.register_command_handler('/a', a_handler)
    dispatcher.register_command_handler('/b', b_handler)

    asyncio.run(dispatcher.handle(a_command_update))
    assert calls[-1] is a_handler
    assert updates[-1] is a_command_update

    asyncio.run(dispatcher.handle(b_command_update))
    assert calls[-1] is b_handler
    assert updates[-1] is b_command_update

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(message_update))
    assert before_calls_counter == len(calls)

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(c_command_update))
    assert before_calls_counter == len(calls)

    dispatcher.register_command_handler('/c', c_handler)
    asyncio.run(dispatcher.handle(c_command_update))
    assert calls[-1] is c_handler
    assert updates[-1] is c_command_update


def test_callbacks(dispatcher):
    a_callback_update = utils.callback_update_by_data('a')
    b_callback_update = utils.callback_update_by_data('b')
    c_callback_update = utils.callback_update_by_data('c')
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def a_handler(c, u):
        updates.append(u)
        calls.append(a_handler)

    async def b_handler(c, u):
        updates.append(u)
        calls.append(b_handler)

    async def c_handler(c, u):
        updates.append(u)
        calls.append(c_handler)

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(a_callback_update))
    asyncio.run(dispatcher.handle(b_callback_update))
    asyncio.run(dispatcher.handle(c_callback_update))
    assert before_calls_counter == len(calls)

    dispatcher.register_callback_handler('a', a_handler)
    dispatcher.register_callback_handler('b', b_handler)

    asyncio.run(dispatcher.handle(a_callback_update))
    assert calls[-1] is a_handler
    assert updates[-1] is a_callback_update

    asyncio.run(dispatcher.handle(b_callback_update))
    assert calls[-1] is b_handler
    assert updates[-1] is b_callback_update

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(message_update))
    assert before_calls_counter == len(calls)

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(c_callback_update))
    assert before_calls_counter == len(calls)

    dispatcher.register_callback_handler('c', c_handler)
    asyncio.run(dispatcher.handle(c_callback_update))
    assert calls[-1] is c_handler
    assert updates[-1] is c_callback_update


def test_inline_query(dispatcher):
    a_inline_query_update = utils.inline_query_update_by_query('a')
    b_inline_query_update = utils.inline_query_update_by_query('b')
    c_inline_query_update = utils.inline_query_update_by_query('c')
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def a_handler(c, u):
        updates.append(u)
        calls.append(a_handler)

    async def b_handler(c, u):
        updates.append(u)
        calls.append(b_handler)

    async def c_handler(c, u):
        updates.append(u)
        calls.append(c_handler)

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(a_inline_query_update))
    asyncio.run(dispatcher.handle(b_inline_query_update))
    asyncio.run(dispatcher.handle(c_inline_query_update))
    assert before_calls_counter == len(calls)

    dispatcher.register_inline_handler('a', a_handler)
    dispatcher.register_inline_handler('b', b_handler)

    asyncio.run(dispatcher.handle(a_inline_query_update))
    assert calls[-1] is a_handler
    assert updates[-1] is a_inline_query_update

    asyncio.run(dispatcher.handle(b_inline_query_update))
    assert calls[-1] is b_handler
    assert updates[-1] is b_inline_query_update

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(message_update))
    assert before_calls_counter == len(calls)

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(c_inline_query_update))
    assert before_calls_counter == len(calls)

    dispatcher.register_inline_handler('c', c_handler)
    asyncio.run(dispatcher.handle(c_inline_query_update))
    assert calls[-1] is c_handler
    assert updates[-1] is c_inline_query_update


def test_chosen_inline_result(dispatcher):
    chosen_inline_result_update = utils.chosen_inline_result_update()

    calls = list()
    updates = list()

    async def chosen_inline_result_handler(c, u):
        updates.append(u)
        calls.append(chosen_inline_result_handler)

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(chosen_inline_result_update))
    assert before_calls_counter == len(calls)
    dispatcher.register_chosen_inline_result_handler(chosen_inline_result_handler)
    asyncio.run(dispatcher.handle(chosen_inline_result_update))
    assert calls[-1] is chosen_inline_result_handler
    assert updates[-1] is chosen_inline_result_update


def test_edited_message(dispatcher):
    edited_message_update = utils.edited_message_update_by_text('abc')

    calls = list()
    updates = list()

    async def edited_message_handler(c, u):
        updates.append(u)
        calls.append(edited_message_handler)

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(edited_message_update))
    assert before_calls_counter == len(calls)
    dispatcher.register_edited_message_handler(edited_message_handler)
    asyncio.run(dispatcher.handle(edited_message_update))
    assert calls[-1] is edited_message_handler
    assert updates[-1] is edited_message_update


def test_channel_post(dispatcher):
    channel_post_update = utils.channel_post_update()

    calls = list()
    updates = list()

    async def channel_post_handler(c, u):
        updates.append(u)
        calls.append(channel_post_handler)

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(channel_post_update))
    assert before_calls_counter == len(calls)
    dispatcher.register_channel_post_handler(channel_post_handler)
    asyncio.run(dispatcher.handle(channel_post_update))
    assert calls[-1] is channel_post_handler
    assert updates[-1] is channel_post_update


def test_edited_channel_post(dispatcher):
    edited_channel_post_update = utils.edited_channel_post_update()

    calls = list()
    updates = list()

    async def edited_channel_post_handler(c, u):
        updates.append(u)
        calls.append(edited_channel_post_handler)

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(edited_channel_post_update))
    assert before_calls_counter == len(calls)
    dispatcher.register_edited_channel_post_handler(edited_channel_post_handler)
    asyncio.run(dispatcher.handle(edited_channel_post_update))
    assert calls[-1] is edited_channel_post_handler
    assert updates[-1] is edited_channel_post_update


def test_dice(dispatcher):
    dice_update = utils.dice_update()
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def dice_handler(c, u):
        updates.append(u)
        calls.append(dice_handler)

    async def message_handler(c, u):
        updates.append(u)
        calls.append(message_handler)

    dispatcher.register_message_handler(re.compile('.*'), message_handler)
    asyncio.run(dispatcher.handle(message_update))
    asyncio.run(dispatcher.handle(dice_update))
    assert calls[-1] is message_handler
    assert updates[-1] is message_update
    dispatcher.register_dice_handler(dice_handler)
    asyncio.run(dispatcher.handle(dice_update))
    assert calls[-1] is dice_handler
    assert updates[-1] is dice_update


def test_document(dispatcher):
    document_update = utils.document_update()
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def document_handler(c, u):
        updates.append(u)
        calls.append(document_handler)

    async def message_handler(c, u):
        updates.append(u)
        calls.append(message_handler)

    dispatcher.register_message_handler(re.compile('.*'), message_handler)
    asyncio.run(dispatcher.handle(message_update))
    asyncio.run(dispatcher.handle(document_update))
    assert calls[-1] is message_handler
    assert updates[-1] is message_update
    dispatcher.register_document_handler(document_handler)
    asyncio.run(dispatcher.handle(document_update))
    assert calls[-1] is document_handler
    assert updates[-1] is document_update


def test_animation(dispatcher):
    animation_update = utils.animation_update()
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def animation_handler(c, u):
        updates.append(u)
        calls.append(animation_handler)

    async def message_handler(c, u):
        updates.append(u)
        calls.append(message_handler)

    dispatcher.register_message_handler(re.compile('.*'), message_handler)
    asyncio.run(dispatcher.handle(message_update))
    asyncio.run(dispatcher.handle(animation_update))
    assert calls[-1] is message_handler
    assert updates[-1] is message_update
    dispatcher.register_animation_handler(animation_handler)
    asyncio.run(dispatcher.handle(animation_update))
    assert calls[-1] is animation_handler
    assert updates[-1] is animation_update


def test_animation_document_conflict(dispatcher):
    animation_update = utils.animation_update()
    document_update = utils.document_update()

    calls = list()
    updates = list()

    async def animation_handler(c, u):
        updates.append(u)
        calls.append(animation_handler)

    async def document_handler(c, u):
        updates.append(u)
        calls.append(document_handler)

    dispatcher.register_document_handler(document_handler)
    asyncio.run(dispatcher.handle(document_update))
    asyncio.run(dispatcher.handle(animation_update))
    assert calls[-1] is document_handler
    assert updates[-1] is document_update
    dispatcher.register_animation_handler(animation_handler)
    asyncio.run(dispatcher.handle(animation_update))
    assert calls[-1] is animation_handler
    assert updates[-1] is animation_update
    asyncio.run(dispatcher.handle(document_update))
    assert calls[-1] is document_handler
    assert updates[-1] is document_update


def test_audio(dispatcher):
    audio_update = utils.audio_update()
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def audio_handler(c, u):
        updates.append(u)
        calls.append(audio_handler)

    async def message_handler(c, u):
        updates.append(u)
        calls.append(message_handler)

    dispatcher.register_message_handler(re.compile('.*'), message_handler)
    asyncio.run(dispatcher.handle(message_update))
    asyncio.run(dispatcher.handle(audio_update))
    assert calls[-1] is message_handler
    assert updates[-1] is message_update
    dispatcher.register_audio_handler(audio_handler)
    asyncio.run(dispatcher.handle(audio_update))
    assert calls[-1] is audio_handler
    assert updates[-1] is audio_update


def test_contact(dispatcher):
    contact_update = utils.contact_update()
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def contact_handler(c, u):
        updates.append(u)
        calls.append(contact_handler)

    async def message_handler(c, u):
        updates.append(u)
        calls.append(message_handler)

    dispatcher.register_message_handler(re.compile('.*'), message_handler)
    asyncio.run(dispatcher.handle(message_update))
    asyncio.run(dispatcher.handle(contact_update))
    assert calls[-1] is message_handler
    assert updates[-1] is message_update
    dispatcher.register_contact_handler(contact_handler)
    asyncio.run(dispatcher.handle(contact_update))
    assert calls[-1] is contact_handler
    assert updates[-1] is contact_update


def test_new_chat_members(dispatcher):
    new_chat_members_update = utils.new_chat_members_update()
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def new_chat_members_handler(c, u):
        updates.append(u)
        calls.append(new_chat_members_handler)

    async def message_handler(c, u):
        updates.append(u)
        calls.append(message_handler)

    dispatcher.register_message_handler(re.compile('.*'), message_handler)
    asyncio.run(dispatcher.handle(message_update))
    asyncio.run(dispatcher.handle(new_chat_members_update))
    assert calls[-1] is message_handler
    assert updates[-1] is message_update
    dispatcher.register_new_chat_members_handler(new_chat_members_handler)
    asyncio.run(dispatcher.handle(new_chat_members_update))
    assert calls[-1] is new_chat_members_handler
    assert updates[-1] is new_chat_members_update


def test_new_chat_title(dispatcher):
    new_chat_title_update = utils.new_chat_title_update()
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def new_chat_title_handler(c, u):
        updates.append(u)
        calls.append(new_chat_title_handler)

    async def message_handler(c, u):
        updates.append(u)
        calls.append(message_handler)

    dispatcher.register_message_handler(re.compile('.*'), message_handler)
    asyncio.run(dispatcher.handle(message_update))
    asyncio.run(dispatcher.handle(new_chat_title_update))
    assert calls[-1] is message_handler
    assert updates[-1] is message_update
    dispatcher.register_new_chat_title_handler(new_chat_title_handler)
    asyncio.run(dispatcher.handle(new_chat_title_update))
    assert calls[-1] is new_chat_title_handler
    assert updates[-1] is new_chat_title_update


def test_new_chat_photo(dispatcher):
    new_chat_photo_update = utils.new_chat_photo_update()
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def new_chat_photo_handler(c, u):
        updates.append(u)
        calls.append(new_chat_photo_handler)

    async def message_handler(c, u):
        updates.append(u)
        calls.append(message_handler)

    dispatcher.register_message_handler(re.compile('.*'), message_handler)
    asyncio.run(dispatcher.handle(message_update))
    asyncio.run(dispatcher.handle(new_chat_photo_update))
    assert calls[-1] is message_handler
    assert updates[-1] is message_update
    dispatcher.register_new_chat_photo_handler(new_chat_photo_handler)
    asyncio.run(dispatcher.handle(new_chat_photo_update))
    assert calls[-1] is new_chat_photo_handler
    assert updates[-1] is new_chat_photo_update


def test_left_chat_member(dispatcher):
    left_chat_member_update = utils.left_chat_member_update()
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def left_chat_member_handler(c, u):
        updates.append(u)
        calls.append(left_chat_member_handler)

    async def message_handler(c, u):
        updates.append(u)
        calls.append(message_handler)

    dispatcher.register_message_handler(re.compile('.*'), message_handler)
    asyncio.run(dispatcher.handle(message_update))
    asyncio.run(dispatcher.handle(left_chat_member_update))
    assert calls[-1] is message_handler
    assert updates[-1] is message_update
    dispatcher.register_left_chat_member_handler(left_chat_member_handler)
    asyncio.run(dispatcher.handle(left_chat_member_update))
    assert calls[-1] is left_chat_member_handler
    assert updates[-1] is left_chat_member_update


def test_location(dispatcher):
    location_update = utils.location_update()
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def location_handler(c, u):
        updates.append(u)
        calls.append(location_handler)

    async def message_handler(c, u):
        updates.append(u)
        calls.append(message_handler)

    dispatcher.register_message_handler(re.compile('.*'), message_handler)
    asyncio.run(dispatcher.handle(message_update))
    asyncio.run(dispatcher.handle(location_update))
    assert calls[-1] is message_handler
    assert updates[-1] is message_update
    dispatcher.register_location_handler(location_handler)
    asyncio.run(dispatcher.handle(location_update))
    assert calls[-1] is location_handler
    assert updates[-1] is location_update


def test_poll(dispatcher):
    poll_update = utils.poll_update()

    calls = list()
    updates = list()

    async def poll_handler(c, u):
        updates.append(u)
        calls.append(poll_handler)

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(poll_update))
    assert before_calls_counter == len(calls)
    dispatcher.register_poll_handler(poll_handler)
    asyncio.run(dispatcher.handle(poll_update))
    assert calls[-1] is poll_handler
    assert updates[-1] is poll_update


def test_poll_answer(dispatcher):
    poll_answer_update = utils.poll_answer_update()

    calls = list()
    updates = list()

    async def poll_answer_handler(c, u):
        updates.append(u)
        calls.append(poll_answer_handler)

    before_calls_counter = len(calls)
    asyncio.run(dispatcher.handle(poll_answer_update))
    assert before_calls_counter == len(calls)
    dispatcher.register_poll_answer_handler(poll_answer_handler)
    asyncio.run(dispatcher.handle(poll_answer_update))
    assert calls[-1] is poll_answer_handler
    assert updates[-1] is poll_answer_update


def test_photo(dispatcher):
    photo_update = utils.photo_update()
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def photo_handler(c, u):
        updates.append(u)
        calls.append(photo_handler)

    async def message_handler(c, u):
        updates.append(u)
        calls.append(message_handler)

    dispatcher.register_message_handler(re.compile('.*'), message_handler)
    asyncio.run(dispatcher.handle(message_update))
    asyncio.run(dispatcher.handle(photo_update))
    assert calls[-1] is message_handler
    assert updates[-1] is message_update
    dispatcher.register_photo_handler(photo_handler)
    asyncio.run(dispatcher.handle(photo_update))
    assert calls[-1] is photo_handler
    assert updates[-1] is photo_update


def test_sticker(dispatcher):
    sticker_update = utils.sticker_update()
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def sticker_handler(c, u):
        updates.append(u)
        calls.append(sticker_handler)

    async def message_handler(c, u):
        updates.append(u)
        calls.append(message_handler)

    dispatcher.register_message_handler(re.compile('.*'), message_handler)
    asyncio.run(dispatcher.handle(message_update))
    asyncio.run(dispatcher.handle(sticker_update))
    assert calls[-1] is message_handler
    assert updates[-1] is message_update
    dispatcher.register_sticker_handler(sticker_handler)
    asyncio.run(dispatcher.handle(sticker_update))
    assert calls[-1] is sticker_handler
    assert updates[-1] is sticker_update


def test_video(dispatcher):
    video_update = utils.video_update()
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def video_handler(c, u):
        updates.append(u)
        calls.append(video_handler)

    async def message_handler(c, u):
        updates.append(u)
        calls.append(message_handler)

    dispatcher.register_message_handler(re.compile('.*'), message_handler)
    asyncio.run(dispatcher.handle(message_update))
    asyncio.run(dispatcher.handle(video_update))
    assert calls[-1] is message_handler
    assert updates[-1] is message_update
    dispatcher.register_video_handler(video_handler)
    asyncio.run(dispatcher.handle(video_update))
    assert calls[-1] is video_handler
    assert updates[-1] is video_update


def test_video_note(dispatcher):
    video_note_update = utils.video_note_update()
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def video_note_handler(c, u):
        updates.append(u)
        calls.append(video_note_handler)

    async def message_handler(c, u):
        updates.append(u)
        calls.append(message_handler)

    dispatcher.register_message_handler(re.compile('.*'), message_handler)
    asyncio.run(dispatcher.handle(message_update))
    asyncio.run(dispatcher.handle(video_note_update))
    assert calls[-1] is message_handler
    assert updates[-1] is message_update
    dispatcher.register_video_note_handler(video_note_handler)
    asyncio.run(dispatcher.handle(video_note_update))
    assert calls[-1] is video_note_handler
    assert updates[-1] is video_note_update


def test_voice(dispatcher):
    voice_update = utils.voice_update()
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def voice_handler(c, u):
        updates.append(u)
        calls.append(voice_handler)

    async def message_handler(c, u):
        updates.append(u)
        calls.append(message_handler)

    dispatcher.register_message_handler(re.compile('.*'), message_handler)
    asyncio.run(dispatcher.handle(message_update))
    asyncio.run(dispatcher.handle(voice_update))
    assert calls[-1] is message_handler
    assert updates[-1] is message_update
    dispatcher.register_voice_handler(voice_handler)
    asyncio.run(dispatcher.handle(voice_update))
    assert calls[-1] is voice_handler
    assert updates[-1] is voice_update


def test_venue(dispatcher):
    venue_update = utils.venue_update()
    message_update = utils.message_update_by_text('message')

    calls = list()
    updates = list()

    async def venue_handler(c, u):
        updates.append(u)
        calls.append(venue_handler)

    async def message_handler(c, u):
        updates.append(u)
        calls.append(message_handler)

    dispatcher.register_message_handler(re.compile('.*'), message_handler)
    asyncio.run(dispatcher.handle(message_update))
    asyncio.run(dispatcher.handle(venue_update))
    assert calls[-1] is message_handler
    assert updates[-1] is message_update
    dispatcher.register_venue_handler(venue_handler)
    asyncio.run(dispatcher.handle(venue_update))
    assert calls[-1] is venue_handler
    assert updates[-1] is venue_update


def test_match_sequence(dispatcher):
    abc_message_update = utils.message_update_by_text('abc')

    updates = list()
    calls = list()

    async def universal_handler(c, u):
        updates.append(u)
        calls.append(universal_handler)

    async def abc_handler(c, u):
        updates.append(u)
        calls.append(abc_handler)

    dispatcher.register_message_handler(re.compile('.*'), universal_handler)
    dispatcher.register_message_handler('abc', abc_handler)
    asyncio.run(dispatcher.handle(abc_message_update))
    assert calls[-1] is abc_handler
    assert updates[-1] is abc_message_update

# TODO test_pre_checkout_query
# TODO test_shipping_query
# TODO test_connected_website
# TODO test_game
# TODO test_invoice
# TODO test_passport_data
# TODO test_successful_payment
