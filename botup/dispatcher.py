import threading

try:
    import ujson as json
except ImportError:
    import json

from . import handlers
from .types import Update


class Dispatcher:

    def __init__(self):
        self.statements = set()
        self.commands = dict()
        self.callbacks = dict()
        self.messages = dict()
        self.inlines = dict()
        self.channel_post_handler = None
        self.chosen_inline_result_handler = None
        self.edited_channel_post_handler = None
        self.edited_message_handler = None
        self.poll_handler = None
        self.pre_checkout_query_handler = None
        self.shipping_query_handler = None
        self.document_handler = None
        self.animation_handler = None
        self.audio_handler = None
        self.connected_website_handler = None
        self.contact_handler = None
        self.game_handler = None
        self.invoice_handler = None
        self.left_chat_member_handler = None
        self.location_handler = None
        self.new_chat_members_handler = None
        self.new_chat_photo_handler = None
        self.new_chat_title_handler = None
        self.passport_data_handler = None
        self.photo_handler = None
        self.sticker_handler = None
        self.successful_payment_handler = None
        self.venue_handler = None
        self.video_handler = None
        self.video_note_handler = None
        self.voice_handler = None

    def register_command_handler(self, command, handler):
        assert isinstance(command, str), 'command is not a str type'
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_command)
        if not command.startswith('/'):
            command = f'/{command}'
        self.commands[command] = handler

    def register_message_handler(self, message, handler):
        assert isinstance(message, str), 'message is not a str type'
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_message)
        self.messages[message] = handler

    def register_callback_handler(self, callback, handler):
        assert isinstance(callback, str), 'callback is not a str type'
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_callback)
        self.callbacks[callback] = handler

    def register_inline_handler(self, inline_query, handler):
        assert isinstance(inline_query, str), 'inline_query is not a str type'
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_inline)
        self.inlines[inline_query] = handler

    def register_channel_post_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_channel_post)
        self.channel_post_handler = handler

    def register_edited_message_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_edited_message)
        self.edited_message_handler = handler

    def register_edited_channel_post_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_edited_channel_post)
        self.edited_channel_post_handler = handler

    def register_chosen_inline_result_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_chosen_inline_result)
        self.chosen_inline_result_handler = handler

    def register_shipping_query_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_shipping_query)
        self.shipping_query_handler = handler

    def register_pre_checkout_query_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_pre_checkout_query)
        self.pre_checkout_query_handler = handler

    def register_poll_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_poll)
        self.poll_handler = handler

    def register_document_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_document)
        self.document_handler = handler

    def register_animation_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_animation)
        self.animation_handler = handler

    def register_audio_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_audio)
        self.audio_handler = handler

    def register_connected_website_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_connected_website)
        self.connected_website_handler = handler

    def register_contact_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_contact)
        self.contact_handler = handler

    def register_game_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_game)
        self.game_handler = handler

    def register_invoice_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_invoice)
        self.invoice_handler = handler

    def register_left_chat_member_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_left_chat_member)
        self.left_chat_member_handler = handler

    def register_location_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_location)
        self.location_handler = handler

    def register_new_chat_members_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_new_chat_members)
        self.new_chat_members_handler = handler

    def register_new_chat_photo_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_new_chat_photo)
        self.new_chat_photo_handler = handler

    def register_new_chat_title_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_new_chat_title)
        self.new_chat_title_handler = handler

    def register_passport_data_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_passport_data)
        self.passport_data_handler = handler

    def register_photo_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_photo)
        self.photo_handler = handler

    def register_sticker_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_sticker)
        self.sticker_handler = handler

    def register_successful_payment_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_successful_payment)
        self.successful_payment_handler = handler

    def register_venue_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_venue)
        self.venue_handler = handler

    def register_video_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_video)
        self.video_handler = handler

    def register_video_note_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_video_note)
        self.video_note_handler = handler

    def register_voice_handler(self, handler):
        assert callable(handler), 'handler is not a function type'
        self.statements.add(self._is_voice)
        self.voice_handler = handler

    def _is_command(self, update):
        if update.message and update.message.text and update.message.text.startswith('/'):
            handlers.CommandHandler(update, self.commands).handle()

    def _is_message(self, update):
        if update.message and update.message.text and not update.message.text.startswith('/'):
            handlers.MessageHandler(update, self.messages).handle()

    def _is_callback(self, update):
        if update.callback_query:
            handlers.CallbackQueryHandler(update, self.callbacks).handle()

    def _is_inline(self, update):
        if update.inline_query:
            handlers.InlineQueryHandler(update, self.inlines).handle()

    def _is_channel_post(self, update):
        if update.channel_post:
            handlers.ChannelPostHandler(update, self.channel_post_handler).handle()

    def _is_edited_message(self, update):
        if update.edited_message:
            handlers.EditedMessageHandler(update, self.edited_message_handler).handle()

    def _is_edited_channel_post(self, update):
        if update.edited_channel_post:
            handlers.EditedChannelPostHandler(update, self.edited_channel_post_handler).handle()

    def _is_chosen_inline_result(self, update):
        if update.chosen_inline_result:
            handlers.ChosenInlineResultHandler(update, self.chosen_inline_result_handler).handle()

    def _is_shipping_query(self, update):
        if update.shipping_query:
            handlers.ShippingQueryHandler(update, self.shipping_query_handler).handle()

    def _is_pre_checkout_query(self, update):
        if update.pre_checkout_query:
            handlers.PreCheckoutQueryHandler(update, self.pre_checkout_query_handler).handle()

    def _is_poll(self, update):
        if update.poll:
            handlers.PollHandler(update, self.poll_handler).handle()

    def _is_document(self, update):
        if update.message and update.message.document:
            handlers.DocumentHandler(update, self.document_handler).handle()

    def _is_animation(self, update):
        if update.message and update.message.animation:
            handlers.AnimationHandler(update, self.animation_handler).handle()

    def _is_audio(self, update):
        if update.message and update.message.audio:
            handlers.AudioHandler(update, self.audio_handler).handle()

    def _is_connected_website(self, update):
        if update.message and update.message.connected_website:
            handlers.ConnectedWebsiteHandler(update, self.connected_website_handler).handle()

    def _is_contact(self, update):
        if update.message and update.message.contact:
            handlers.ContactHandler(update, self.contact_handler).handle()

    def _is_game(self, update):
        if update.message and update.message.game:
            handlers.GameHandler(update, self.game_handler).handle()

    def _is_invoice(self, update):
        if update.message and update.message.invoice:
            handlers.InvoiceHandler(update, self.invoice_handler).handle()

    def _is_left_chat_member(self, update):
        if update.message and update.message.left_chat_member:
            handlers.LeftChatMemberHandler(update, self.left_chat_member_handler).handle()

    def _is_location(self, update):
        if update.message and update.message.location:
            handlers.LocationHandler(update, self.location_handler).handle()

    def _is_new_chat_members(self, update):
        if update.message and update.message.new_chat_members:
            handlers.NewChatMembersHandler(update, self.new_chat_members_handler).handle()

    def _is_new_chat_photo(self, update):
        if update.message and update.message.new_chat_photo:
            handlers.NewChatPhotoHandler(update, self.new_chat_photo_handler).handle()

    def _is_new_chat_title(self, update):
        if update.message and update.message.new_chat_title:
            handlers.NewChatTitleHandler(update, self.new_chat_title_handler).handle()

    def _is_passport_data(self, update):
        if update.message and update.message.passport_data:
            handlers.PassportDataHandler(update, self.passport_data_handler).handle()

    def _is_photo(self, update):
        if update.message and update.message.photo:
            handlers.PhotoHandler(update, self.photo_handler).handle()

    def _is_sticker(self, update):
        if update.message and update.message.sticker:
            handlers.StickerHandler(update, self.sticker_handler).handle()

    def _is_successful_payment(self, update):
        if update.message and update.message.successful_payment:
            handlers.SuccessfulPaymentHandler(update, self.successful_payment_handler).handle()

    def _is_venue(self, update):
        if update.message and update.message.venue:
            handlers.VenueHandler(update, self.venue_handler).handle()

    def _is_video(self, update):
        if update.message and update.message.video:
            handlers.VideoHandler(update, self.video_handler).handle()

    def _is_video_note(self, update):
        if update.message and update.message.video_note:
            handlers.VideoNoteHandler(update, self.video_note_handler).handle()

    def _is_voice(self, update):
        if update.message and update.message.voice:
            handlers.VoiceHandler(update, self.voice_handler).handle()

    def include(self, dispatcher, handler, prefix=None):
        assert isinstance(dispatcher, Dispatcher), 'dispatcher is not a Dispatcher type'
        assert callable(handler), 'handler is not a function type'
        debug = False
        if prefix:
            assert isinstance(prefix, (str, int)), 'prefix is not a str or int type'
            debug = True

        for key in dispatcher.messages:
            if key in self.messages and debug:
                print(f'{prefix}:Handler for message "{key}" has been replaced')
            self.register_message_handler(key, handler)
        for key in dispatcher.commands:
            if key in self.commands and debug:
                print(f'{prefix}:Handler for command "{key}" has been replaced')
            self.register_command_handler(key, handler)
        for key in dispatcher.callbacks:
            if key in self.callbacks and debug:
                print(f'{prefix}:Handler for callback "{key}" has been replaced')
            self.register_callback_handler(key, handler)
        for key in dispatcher.inlines:
            if key in self.inlines and debug:
                print(f'{prefix}:Handler for inline_query "{key}" has been replaced')
            self.register_inline_handler(key, handler)
        if dispatcher.channel_post_handler:
            if self.channel_post_handler and debug:
                print(f'{prefix}:"channel_post_handler" has been replaced')
            self.register_channel_post_handler(handler)
        if dispatcher.edited_message_handler:
            if self.edited_message_handler and debug:
                print(f'{prefix}:"edited_message_handler" has been replaced')
            self.register_edited_message_handler(handler)
        if dispatcher.edited_channel_post_handler:
            if self.edited_channel_post_handler and debug:
                print(f'{prefix}:"editet_channel_post_handler" has been replaced')
            self.register_edited_channel_post_handler(handler)
        if dispatcher.chosen_inline_result_handler:
            if self.chosen_inline_result_handler and debug:
                print(f'{prefix}:"chosen_inline_result_handler" has been replaced')
            self.register_chosen_inline_result_handler(handler)
        if dispatcher.shipping_query_handler:
            if self.shipping_query_handler and debug:
                print(f'{prefix}:"shipping_query_handler" has been replaced')
            self.register_shipping_query_handler(handler)
        if dispatcher.pre_checkout_query_handler:
            if self.pre_checkout_query_handler and debug:
                print(f'{prefix}:"pre_checkout_query_handler" has been replaced')
            self.register_pre_checkout_query_handler(handler)
        if dispatcher.poll_handler:
            if self.poll_handler and debug:
                print(f'{prefix}:"poll_handler" has been replaced')
            self.register_poll_handler(handler)
        if dispatcher.document_handler:
            if self.document_handler and debug:
                print(f'{prefix}:"document_handler" has been replaced')
            self.register_document_handler(handler)
        if dispatcher.animation_handler:
            if self.animation_handler and debug:
                print(f'{prefix}:"animation_handler" has been replaced')
            self.register_animation_handler(handler)
        if dispatcher.audio_handler:
            if self.audio_handler and debug:
                print(f'{prefix}:"audio_handler" has been replaced')
            self.register_audio_handler(handler)
        if dispatcher.connected_website_handler:
            if self.connected_website_handler and debug:
                print(f'{prefix}:"connected_website_handler" has been replaced')
            self.register_connected_website_handler(handler)
        if dispatcher.contact_handler:
            if self.contact_handler and debug:
                print(f'{prefix}:"contact_handler" has been replaced')
            self.register_contact_handler(handler)
        if dispatcher.game_handler:
            if self.game_handler and debug:
                print(f'{prefix}:"game_handler" has been replaced')
            self.register_game_handler(handler)
        if dispatcher.invoice_handler:
            if self.invoice_handler and debug:
                print(f'{prefix}:"invoice_handler" has been replaced')
            self.register_invoice_handler(handler)
        if dispatcher.left_chat_member_handler:
            if self.left_chat_member_handler and debug:
                print(f'{prefix}:"left_chat_member_handler" has been replaced')
            self.register_left_chat_member_handler(handler)
        if dispatcher.location_handler:
            if self.location_handler and debug:
                print(f'{prefix}:"location_handler" has been replaced')
            self.register_location_handler(handler)
        if dispatcher.new_chat_members_handler:
            if self.new_chat_members_handler and debug:
                print(f'{prefix}:"new_chat_members_handler" has been replaced')
            self.register_new_chat_members_handler(handler)
        if dispatcher.new_chat_photo_handler:
            if self.new_chat_photo_handler and debug:
                print(f'{prefix}:"new_chat_photo_handler" has been replaced')
            self.register_new_chat_photo_handler(handler)
        if dispatcher.new_chat_title_handler:
            if self.new_chat_title_handler and debug:
                print(f'{prefix}:"new_chat_title_handler" has been replaced')
            self.register_new_chat_title_handler(handler)
        if dispatcher.passport_data_handler:
            if self.passport_data_handler and debug:
                print(f'{prefix}:"passport_data_handler" has been replaced')
            self.register_passport_data_handler(handler)
        if dispatcher.photo_handler:
            if self.photo_handler and debug:
                print(f'{prefix}:"photo_handler" has been replaced')
            self.register_photo_handler(handler)
        if dispatcher.sticker_handler:
            if self.sticker_handler and debug:
                print(f'{prefix}:"sticker_handler" has been replaced')
            self.register_sticker_handler(handler)
        if dispatcher.successful_payment_handler:
            if self.successful_payment_handler and debug:
                print(f'{prefix}:"successful_payment_handler" has been replaced')
            self.register_successful_payment_handler(handler)
        if dispatcher.venue_handler:
            if self.venue_handler and debug:
                print(f'{prefix}:"venue_handler" has been replaced')
            self.register_venue_handler(handler)
        if dispatcher.video_handler:
            if self.video_handler and debug:
                print(f'{prefix}:"video_handler" has been replaced')
            self.register_video_handler(handler)
        if dispatcher.video_note_handler:
            if self.video_note_handler and debug:
                print(f'{prefix}:"video_note_handler" has been replaced')
            self.register_video_note_handler(handler)
        if dispatcher.voice_handler:
            if self.voice_handler and debug:
                print(f'{prefix}:"voice_handler" has been replaced')
            self.register_voice_handler(handler)

    def handle(self, update):
        if not isinstance(update, Update):
            update = Update(**update)
        for statement in self.statements:
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
