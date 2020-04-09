import re

from botup import handlers


def middleware(u):
    pass


def function(c, u):
    pass


def test_middleware(dispatcher):
    assert not dispatcher._middlewares
    dispatcher.register_middleware(middleware)
    assert len(dispatcher._middlewares) == 1


def test_command_handler(dispatcher):
    assert not dispatcher._commands
    dispatcher.register(handlers.CommandHandler(re.compile('/.*'), function))
    assert len(dispatcher._commands) == 1


def test_message_handler(dispatcher):
    assert not dispatcher._messages
    dispatcher.register(handlers.MessageHandler('message', function))
    assert len(dispatcher._messages) == 1


def test_callback_handler(dispatcher):
    assert not dispatcher._callbacks
    dispatcher.register(handlers.CallbackQueryHandler('callback_data', function))
    assert len(dispatcher._callbacks) == 1


def test_inline_query_handler(dispatcher):
    assert not dispatcher._inlines
    dispatcher.register(handlers.InlineQueryHandler('inline_query', function))
    assert len(dispatcher._inlines) == 1


def test_channel_post_handler(dispatcher):
    assert not dispatcher._channel_post_handler
    dispatcher.register(handlers.ChannelPostHandler(function))
    assert dispatcher._channel_post_handler


def test_chosen_inline_result_handler(dispatcher):
    assert not dispatcher._chosen_inline_result_handler
    dispatcher.register(handlers.ChosenInlineResultHandler(function))
    assert dispatcher._chosen_inline_result_handler


def test_edited_channel_post_handler(dispatcher):
    assert not dispatcher._edited_channel_post_handler
    dispatcher.register(handlers.EditedChannelPostHandler(function))
    assert dispatcher._edited_channel_post_handler


def test_edited_message_handler(dispatcher):
    assert not dispatcher._edited_message_handler
    dispatcher.register(handlers.EditedMessageHandler(function))
    assert dispatcher._edited_message_handler


def test_poll_handler(dispatcher):
    assert not dispatcher._poll_handler
    dispatcher.register(handlers.PollHandler(function))
    assert dispatcher._poll_handler


def test_poll_answer_handler(dispatcher):
    assert not dispatcher._poll_answer_handler
    dispatcher.register(handlers.PollAnswerHandler(function))
    assert dispatcher._poll_answer_handler


def test_pre_checkout_query_handler(dispatcher):
    assert not dispatcher._pre_checkout_query_handler
    dispatcher.register(handlers.PreCheckoutQueryHandler(function))
    assert dispatcher._pre_checkout_query_handler


def test_shipping_query_handler(dispatcher):
    assert not dispatcher._shipping_query_handler
    dispatcher.register(handlers.ShippingQueryHandler(function))
    assert dispatcher._shipping_query_handler


def test_dice_handler(dispatcher):
    assert not dispatcher._dice_handler
    dispatcher.register(handlers.DiceHandler(function))
    assert dispatcher._dice_handler


def test_document_handler(dispatcher):
    assert not dispatcher._document_handler
    dispatcher.register(handlers.DocumentHandler(function))
    assert dispatcher._document_handler


def test_animation_handler(dispatcher):
    assert not dispatcher._animation_handler
    dispatcher.register(handlers.AnimationHandler(function))
    assert dispatcher._animation_handler


def test_audio_handler(dispatcher):
    assert not dispatcher._audio_handler
    dispatcher.register(handlers.AudioHandler(function))
    assert dispatcher._audio_handler


def test_connected_website_handler(dispatcher):
    assert not dispatcher._connected_website_handler
    dispatcher.register(handlers.ConnectedWebsiteHandler(function))
    assert dispatcher._connected_website_handler


def test_contact_handler(dispatcher):
    assert not dispatcher._contact_handler
    dispatcher.register(handlers.ContactHandler(function))
    assert dispatcher._contact_handler


def test_game_handler(dispatcher):
    assert not dispatcher._game_handler
    dispatcher.register(handlers.GameHandler(function))
    assert dispatcher._game_handler


def test_invoice_handler(dispatcher):
    assert not dispatcher._invoice_handler
    dispatcher.register(handlers.InvoiceHandler(function))
    assert dispatcher._invoice_handler


def test_left_chat_member_handler(dispatcher):
    assert not dispatcher._left_chat_member_handler
    dispatcher.register(handlers.LeftChatMemberHandler(function))
    assert dispatcher._left_chat_member_handler


def test_location_handler(dispatcher):
    assert not dispatcher._location_handler
    dispatcher.register(handlers.LocationHandler(function))
    assert dispatcher._location_handler


def test_new_chat_members_handler(dispatcher):
    assert not dispatcher._new_chat_members_handler
    dispatcher.register(handlers.NewChatMembersHandler(function))
    assert dispatcher._new_chat_members_handler


def test_new_chat_photo_handler(dispatcher):
    assert not dispatcher._new_chat_photo_handler
    dispatcher.register(handlers.NewChatPhotoHandler(function))
    assert dispatcher._new_chat_photo_handler


def test_new_chat_title_handler(dispatcher):
    assert not dispatcher._new_chat_title_handler
    dispatcher.register(handlers.NewChatTitleHandler(function))
    assert dispatcher._new_chat_title_handler


def test_passport_data_handler(dispatcher):
    assert not dispatcher._passport_data_handler
    dispatcher.register(handlers.PassportDataHandler(function))
    assert dispatcher._passport_data_handler


def test_photo_handler(dispatcher):
    assert not dispatcher._photo_handler
    dispatcher.register(handlers.PhotoHandler(function))
    assert dispatcher._photo_handler


def test_sticker_handler(dispatcher):
    assert not dispatcher._sticker_handler
    dispatcher.register(handlers.StickerHandler(function))
    assert dispatcher._sticker_handler


def test_successful_payment_handler(dispatcher):
    assert not dispatcher._successful_payment_handler
    dispatcher.register(handlers.SuccessfulPaymentHandler(function))
    assert dispatcher._successful_payment_handler


def test_venue_handler(dispatcher):
    assert not dispatcher._venue_handler
    dispatcher.register(handlers.VenueHandler(function))
    assert dispatcher._venue_handler


def test_video_handler(dispatcher):
    assert not dispatcher._video_handler
    dispatcher.register(handlers.VideoHandler(function))
    assert dispatcher._video_handler


def test_video_note_handler(dispatcher):
    assert not dispatcher._video_note_handler
    dispatcher.register(handlers.VideoNoteHandler(function))
    assert dispatcher._video_note_handler


def test_voice_handler(dispatcher):
    assert not dispatcher._voice_handler
    dispatcher.register(handlers.VoiceHandler(function))
    assert dispatcher._voice_handler
