import threading

try:
    import ujson as json
except ImportError:
    import json

from . import handlers
from .types import Update


class Bot:

    def __init__(self):
        self._statements = set()
        self._commands = dict()
        self._callbacks = dict()
        self._messages = dict()
        self._inlines = dict()
        self._channel_post_handler = None
        self._chosen_inline_result_handler = None
        self._edited_channel_post_handler = None
        self._edited_message_handler = None
        self._poll_handler = None
        self._pre_checkout_query_handler = None
        self._shipping_query_handler = None
        self._document_handler = None
        self._animation_handler = None
        self._audio_handler = None
        self._connected_website_handler = None
        self._contact_handler = None
        self._game_handler = None
        self._invoice_handler = None
        self._left_chat_member_handler = None
        self._location_handler = None
        self._new_chat_members_handler = None
        self._new_chat_photo_handler = None
        self._new_chat_title_handler = None
        self._passport_data_handler = None
        self._photo_handler = None
        self._sticker_handler = None
        self._successful_payment_handler = None
        self._venue_handler = None
        self._video_handler = None
        self._video_note_handler = None
        self._voice_handler = None

    def register_command_handler(self, command, handler):
        self._statements.add(self._is_command)
        if not command.startswith('/'):
            command = f'/{command}'
        self._commands[command] = handler

    def register_message_handler(self, message, handler):
        self._statements.add(self._is_message)
        self._messages[message] = handler

    def register_callback_handler(self, callback, handler):
        self._statements.add(self._is_callback)
        self._callbacks[callback] = handler

    def register_inline_handler(self, inline_query, handler):
        self._statements.add(self._is_inline)
        self._inlines[inline_query] = handler

    def register_channel_post_handler(self, handler):
        self._statements.add(self._is_channel_post)
        self._channel_post_handler = handler

    def register_edited_message_handler(self, handler):
        self._statements.add(self._is_edited_message)
        self._edited_message_handler = handler

    def register_edited_channel_post_handler(self, handler):
        self._statements.add(self._is_edited_channel_post)
        self._edited_channel_post_handler = handler

    def register_chosen_inline_result_handler(self, handler):
        self._statements.add(self._is_chosen_inline_result)
        self._chosen_inline_result_handler = handler

    def register_shipping_query_handler(self, handler):
        self._statements.add(self._is_shipping_query)
        self._shipping_query_handler = handler

    def register_pre_checkout_query_handler(self, handler):
        self._statements.add(self._is_pre_checkout_query)
        self._pre_checkout_query_handler = handler

    def register_poll_handler(self, handler):
        self._statements.add(self._is_poll)
        self._poll_handler = handler

    def register_document_handler(self, handler):
        self._statements.add(self._is_document)
        self._document_handler = handler

    def register_animation_handler(self, handler):
        self._statements.add(self._is_animation)
        self._animation_handler = handler

    def register_audio_handler(self, handler):
        self._statements.add(self._is_audio)
        self._audio_handler = handler

    def register_connected_website_handler(self, handler):
        self._statements.add(self._is_connected_website)
        self._connected_website_handler = handler

    def register_contact_handler(self, handler):
        self._statements.add(self._is_contact)
        self._contact_handler = handler

    def register_game_handler(self, handler):
        self._statements.add(self._is_game)
        self._game_handler = handler

    def register_invoice_handler(self, handler):
        self._statements.add(self._is_invoice)
        self._invoice_handler = handler

    def register_left_chat_member_handler(self, handler):
        self._statements.add(self._is_left_chat_member)
        self._left_chat_member_handler = handler

    def register_location_handler(self, handler):
        self._statements.add(self._is_location)
        self._location_handler = handler

    def register_new_chat_members_handler(self, handler):
        self._statements.add(self._is_new_chat_members)
        self._new_chat_members_handler = handler

    def register_new_chat_photo_handler(self, handler):
        self._statements.add(self._is_new_chat_photo)
        self._new_chat_photo_handler = handler

    def register_new_chat_title_handler(self, handler):
        self._statements.add(self._is_new_chat_title)
        self._new_chat_title_handler = handler

    def register_passport_data_handler(self, handler):
        self._statements.add(self._is_passport_data)
        self._passport_data_handler = handler

    def register_photo_handler(self, handler):
        self._statements.add(self._is_photo)
        self._photo_handler = handler

    def register_sticker_handler(self, handler):
        self._statements.add(self._is_sticker)
        self._sticker_handler = handler

    def register_successful_payment_handler(self, handler):
        self._statements.add(self._is_successful_payment)
        self._successful_payment_handler = handler

    def register_venue_handler(self, handler):
        self._statements.add(self._is_venue)
        self._venue_handler = handler

    def register_video_handler(self, handler):
        self._statements.add(self._is_video)
        self._video_handler = handler

    def register_video_note_handler(self, handler):
        self._statements.add(self._is_video_note)
        self._video_note_handler = handler

    def register_voice_handler(self, handler):
        self._statements.add(self._is_voice)
        self._voice_handler = handler

    def _is_command(self, update):
        if update.message and update.message.text and update.message.text.startswith('/'):
            handlers.CommandHandler(update, self._commands).handle()

    def _is_message(self, update):
        if update.message and update.message.text and not update.message.text.startswith('/'):
            handlers.MessageHandler(update, self._messages).handle()

    def _is_callback(self, update):
        if update.callback_query:
            handlers.CallbackQueryHandler(update, self._callbacks).handle()

    def _is_inline(self, update):
        if update.inline_query:
            handlers.InlineQueryHandler(update, self._inlines).handle()

    def _is_channel_post(self, update):
        if update.channel_post:
            handlers.ChannelPostHandler(update, self._channel_post_handler).handle()

    def _is_edited_message(self, update):
        if update.edited_message:
            handlers.EditedMessageHandler(update, self._edited_message_handler).handle()

    def _is_edited_channel_post(self, update):
        if update.edited_channel_post:
            handlers.EditedChannelPostHandler(update, self._edited_channel_post_handler).handle()

    def _is_chosen_inline_result(self, update):
        if update.chosen_inline_result:
            handlers.ChosenInlineResultHandler(update, self._chosen_inline_result_handler).handle()

    def _is_shipping_query(self, update):
        if update.shipping_query:
            handlers.ShippingQueryHandler(update, self._shipping_query_handler).handle()

    def _is_pre_checkout_query(self, update):
        if update.pre_checkout_query:
            handlers.PreCheckoutQueryHandler(update, self._pre_checkout_query_handler).handle()

    def _is_poll(self, update):
        if update.poll:
            handlers.PollHandler(update, self._poll_handler).handle()

    def _is_document(self, update):
        if update.message and update.message.document:
            handlers.DocumentHandler(update, self._document_handler).handle()

    def _is_animation(self, update):
        if update.message and update.message.animation:
            handlers.AnimationHandler(update, self._animation_handler).handle()

    def _is_audio(self, update):
        if update.message and update.message.audio:
            handlers.AudioHandler(update, self._audio_handler).handle()

    def _is_connected_website(self, update):
        if update.message and update.message.connected_website:
            handlers.ConnectedWebsiteHandler(update, self._connected_website_handler).handle()

    def _is_contact(self, update):
        if update.message and update.message.contact:
            handlers.ContactHandler(update, self._contact_handler).handle()

    def _is_game(self, update):
        if update.message and update.message.game:
            handlers.GameHandler(update, self._game_handler).handle()

    def _is_invoice(self, update):
        if update.message and update.message.invoice:
            handlers.InvoiceHandler(update, self._invoice_handler).handle()

    def _is_left_chat_member(self, update):
        if update.message and update.message.left_chat_member:
            handlers.LeftChatMemberHandler(update, self._left_chat_member_handler).handle()

    def _is_location(self, update):
        if update.message and update.message.location:
            handlers.LocationHandler(update, self._location_handler).handle()

    def _is_new_chat_members(self, update):
        if update.message and update.message.new_chat_members:
            handlers.NewChatMembersHandler(update, self._new_chat_members_handler).handle()

    def _is_new_chat_photo(self, update):
        if update.message and update.message.new_chat_photo:
            handlers.NewChatPhotoHandler(update, self._new_chat_photo_handler).handle()

    def _is_new_chat_title(self, update):
        if update.message and update.message.new_chat_title:
            handlers.NewChatTitleHandler(update, self._new_chat_title_handler).handle()

    def _is_passport_data(self, update):
        if update.message and update.message.passport_data:
            handlers.PassportDataHandler(update, self._passport_data_handler).handle()

    def _is_photo(self, update):
        if update.message and update.message.photo:
            handlers.PhotoHandler(update, self._photo_handler).handle()

    def _is_sticker(self, update):
        if update.message and update.message.sticker:
            handlers.StickerHandler(update, self._sticker_handler).handle()

    def _is_successful_payment(self, update):
        if update.message and update.message.successful_payment:
            handlers.SuccessfulPaymentHandler(update, self._successful_payment_handler).handle()

    def _is_venue(self, update):
        if update.message and update.message.venue:
            handlers.VenueHandler(update, self._venue_handler).handle()

    def _is_video(self, update):
        if update.message and update.message.video:
            handlers.VideoHandler(update, self._video_handler).handle()

    def _is_video_note(self, update):
        if update.message and update.message.video_note:
            handlers.VideoNoteHandler(update, self._video_note_handler).handle()

    def _is_voice(self, update):
        if update.message and update.message.voice:
            handlers.VoiceHandler(update, self._voice_handler).handle()

    def handle(self, request):
        if 'update_id' not in request:
            return
        update = Update(**request)
        for statement in self._statements:
            statement(update)

    def polling(self, form, tick=1.0, limit=None, timeout=None, allowed_updates=None):
        from .form import Form
        assert isinstance(form, Form), 'Wrong type of form. Must be a botup.form.Form'
        last_update_id = 0
        response = form.get_updates(limit=limit, timeout=timeout, allowed_updates=allowed_updates)
        while True:
            response = json.loads(response)
            for update in response['result']:
                last_update_id = update['update_id']
                self.handle(update)
            timer = threading.Timer(tick, lambda *args: None)
            timer.start()
            timer.join()
            response = form.get_updates(
                offset=last_update_id + 1,
                limit=limit,
                timeout=timeout,
                allowed_updates=allowed_updates
            )
