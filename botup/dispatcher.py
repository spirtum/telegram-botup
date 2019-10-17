import threading
import inspect

try:
    import ujson as json
except ImportError:
    import json

from . import handlers
from .types import Update


class Dispatcher:

    def __init__(self):
        self.success = False
        self.middlewares = list()
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

    def register_middleware(self, middleware):
        self._check_function_signature(middleware, 1)
        self.middlewares.append(middleware)

    def register_command_handler(self, command, handler):
        assert isinstance(command, str), 'command is not a str type'
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_command)
        if not command.startswith('/'):
            command = f'/{command}'
        self.commands[command] = handler

    def register_message_handler(self, message, handler):
        assert isinstance(message, str), 'message is not a str type'
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_message)
        self.messages[message] = handler

    def register_callback_handler(self, callback, handler):
        assert isinstance(callback, str), 'callback is not a str type'
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_callback)
        self.callbacks[callback] = handler

    def register_inline_handler(self, inline_query, handler):
        assert isinstance(inline_query, str), 'inline_query is not a str type'
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_inline)
        self.inlines[inline_query] = handler

    def register_channel_post_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_channel_post)
        self.channel_post_handler = handler

    def register_edited_message_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_edited_message)
        self.edited_message_handler = handler

    def register_edited_channel_post_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_edited_channel_post)
        self.edited_channel_post_handler = handler

    def register_chosen_inline_result_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_chosen_inline_result)
        self.chosen_inline_result_handler = handler

    def register_shipping_query_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_shipping_query)
        self.shipping_query_handler = handler

    def register_pre_checkout_query_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_pre_checkout_query)
        self.pre_checkout_query_handler = handler

    def register_poll_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_poll)
        self.poll_handler = handler

    def register_document_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_document)
        self.document_handler = handler

    def register_animation_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_animation)
        self.animation_handler = handler

    def register_audio_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_audio)
        self.audio_handler = handler

    def register_connected_website_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_connected_website)
        self.connected_website_handler = handler

    def register_contact_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_contact)
        self.contact_handler = handler

    def register_game_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_game)
        self.game_handler = handler

    def register_invoice_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_invoice)
        self.invoice_handler = handler

    def register_left_chat_member_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_left_chat_member)
        self.left_chat_member_handler = handler

    def register_location_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_location)
        self.location_handler = handler

    def register_new_chat_members_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_new_chat_members)
        self.new_chat_members_handler = handler

    def register_new_chat_photo_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_new_chat_photo)
        self.new_chat_photo_handler = handler

    def register_new_chat_title_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_new_chat_title)
        self.new_chat_title_handler = handler

    def register_passport_data_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_passport_data)
        self.passport_data_handler = handler

    def register_photo_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_photo)
        self.photo_handler = handler

    def register_sticker_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_sticker)
        self.sticker_handler = handler

    def register_successful_payment_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_successful_payment)
        self.successful_payment_handler = handler

    def register_venue_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_venue)
        self.venue_handler = handler

    def register_video_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_video)
        self.video_handler = handler

    def register_video_note_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_video_note)
        self.video_note_handler = handler

    def register_voice_handler(self, handler):
        self._check_function_signature(handler, 2)
        self.statements.add(self._is_voice)
        self.voice_handler = handler

    def _is_command(self, update):
        if update.message and update.message.text and update.message.text.startswith('/'):
            self.success = True
            handlers.CommandHandler(update, self.commands).handle()

    def _is_message(self, update):
        if update.message and update.message.text and not update.message.text.startswith('/'):
            self.success = True
            handlers.MessageHandler(update, self.messages).handle()

    def _is_callback(self, update):
        if update.callback_query:
            self.success = True
            handlers.CallbackQueryHandler(update, self.callbacks).handle()

    def _is_inline(self, update):
        if update.inline_query:
            self.success = True
            handlers.InlineQueryHandler(update, self.inlines).handle()

    def _is_channel_post(self, update):
        if update.channel_post:
            self.success = True
            handlers.ChannelPostHandler(update, self.channel_post_handler).handle()

    def _is_edited_message(self, update):
        if update.edited_message:
            self.success = True
            handlers.EditedMessageHandler(update, self.edited_message_handler).handle()

    def _is_edited_channel_post(self, update):
        if update.edited_channel_post:
            self.success = True
            handlers.EditedChannelPostHandler(update, self.edited_channel_post_handler).handle()

    def _is_chosen_inline_result(self, update):
        if update.chosen_inline_result:
            self.success = True
            handlers.ChosenInlineResultHandler(update, self.chosen_inline_result_handler).handle()

    def _is_shipping_query(self, update):
        if update.shipping_query:
            self.success = True
            handlers.ShippingQueryHandler(update, self.shipping_query_handler).handle()

    def _is_pre_checkout_query(self, update):
        if update.pre_checkout_query:
            self.success = True
            handlers.PreCheckoutQueryHandler(update, self.pre_checkout_query_handler).handle()

    def _is_poll(self, update):
        if update.poll:
            self.success = True
            handlers.PollHandler(update, self.poll_handler).handle()

    def _is_document(self, update):
        if update.message and update.message.document:
            self.success = True
            handlers.DocumentHandler(update, self.document_handler).handle()

    def _is_animation(self, update):
        if update.message and update.message.animation:
            self.success = True
            handlers.AnimationHandler(update, self.animation_handler).handle()

    def _is_audio(self, update):
        if update.message and update.message.audio:
            self.success = True
            handlers.AudioHandler(update, self.audio_handler).handle()

    def _is_connected_website(self, update):
        if update.message and update.message.connected_website:
            self.success = True
            handlers.ConnectedWebsiteHandler(update, self.connected_website_handler).handle()

    def _is_contact(self, update):
        if update.message and update.message.contact:
            self.success = True
            handlers.ContactHandler(update, self.contact_handler).handle()

    def _is_game(self, update):
        if update.message and update.message.game:
            self.success = True
            handlers.GameHandler(update, self.game_handler).handle()

    def _is_invoice(self, update):
        if update.message and update.message.invoice:
            self.success = True
            handlers.InvoiceHandler(update, self.invoice_handler).handle()

    def _is_left_chat_member(self, update):
        if update.message and update.message.left_chat_member:
            self.success = True
            handlers.LeftChatMemberHandler(update, self.left_chat_member_handler).handle()

    def _is_location(self, update):
        if update.message and update.message.location:
            self.success = True
            handlers.LocationHandler(update, self.location_handler).handle()

    def _is_new_chat_members(self, update):
        if update.message and update.message.new_chat_members:
            self.success = True
            handlers.NewChatMembersHandler(update, self.new_chat_members_handler).handle()

    def _is_new_chat_photo(self, update):
        if update.message and update.message.new_chat_photo:
            self.success = True
            handlers.NewChatPhotoHandler(update, self.new_chat_photo_handler).handle()

    def _is_new_chat_title(self, update):
        if update.message and update.message.new_chat_title:
            self.success = True
            handlers.NewChatTitleHandler(update, self.new_chat_title_handler).handle()

    def _is_passport_data(self, update):
        if update.message and update.message.passport_data:
            self.success = True
            handlers.PassportDataHandler(update, self.passport_data_handler).handle()

    def _is_photo(self, update):
        if update.message and update.message.photo:
            self.success = True
            handlers.PhotoHandler(update, self.photo_handler).handle()

    def _is_sticker(self, update):
        if update.message and update.message.sticker:
            self.success = True
            handlers.StickerHandler(update, self.sticker_handler).handle()

    def _is_successful_payment(self, update):
        if update.message and update.message.successful_payment:
            self.success = True
            handlers.SuccessfulPaymentHandler(update, self.successful_payment_handler).handle()

    def _is_venue(self, update):
        if update.message and update.message.venue:
            self.success = True
            handlers.VenueHandler(update, self.venue_handler).handle()

    def _is_video(self, update):
        if update.message and update.message.video:
            self.success = True
            handlers.VideoHandler(update, self.video_handler).handle()

    def _is_video_note(self, update):
        if update.message and update.message.video_note:
            self.success = True
            handlers.VideoNoteHandler(update, self.video_note_handler).handle()

    def _is_voice(self, update):
        if update.message and update.message.voice:
            self.success = True
            handlers.VoiceHandler(update, self.voice_handler).handle()

    def include(self, dispatcher):
        for key, handler in dispatcher.messages.items():
            self.register_message_handler(key, handler)
        for key, handler in dispatcher.commands.items():
            self.register_command_handler(key, handler)
        for key, handler in dispatcher.callbacks.items():
            self.register_callback_handler(key, handler)
        for key, handler in dispatcher.inlines.items():
            self.register_inline_handler(key, handler)
        if dispatcher.channel_post_handler:
            self.register_channel_post_handler(dispatcher.channel_post_handler)
        if dispatcher.edited_message_handler:
            self.register_edited_message_handler(dispatcher.edited_message_handler)
        if dispatcher.edited_channel_post_handler:
            self.register_edited_channel_post_handler(dispatcher.edited_channel_post_handler)
        if dispatcher.chosen_inline_result_handler:
            self.register_chosen_inline_result_handler(dispatcher.chosen_inline_result_handler)
        if dispatcher.shipping_query_handler:
            self.register_shipping_query_handler(dispatcher.shipping_query_handler)
        if dispatcher.pre_checkout_query_handler:
            self.register_pre_checkout_query_handler(dispatcher.pre_checkout_query_handler)
        if dispatcher.poll_handler:
            self.register_poll_handler(dispatcher.poll_handler)
        if dispatcher.document_handler:
            self.register_document_handler(dispatcher.document_handler)
        if dispatcher.animation_handler:
            self.register_animation_handler(dispatcher.animation_handler)
        if dispatcher.audio_handler:
            self.register_audio_handler(dispatcher.audio_handler)
        if dispatcher.connected_website_handler:
            self.register_connected_website_handler(dispatcher.connected_website_handler)
        if dispatcher.contact_handler:
            self.register_contact_handler(dispatcher.contact_handler)
        if dispatcher.game_handler:
            self.register_game_handler(dispatcher.game_handler)
        if dispatcher.invoice_handler:
            self.register_invoice_handler(dispatcher.invoice_handler)
        if dispatcher.left_chat_member_handler:
            self.register_left_chat_member_handler(dispatcher.left_chat_member_handler)
        if dispatcher.location_handler:
            self.register_location_handler(dispatcher.location_handler)
        if dispatcher.new_chat_members_handler:
            self.register_new_chat_members_handler(dispatcher.new_chat_members_handler)
        if dispatcher.new_chat_photo_handler:
            self.register_new_chat_photo_handler(dispatcher.new_chat_photo_handler)
        if dispatcher.new_chat_title_handler:
            self.register_new_chat_title_handler(dispatcher.new_chat_title_handler)
        if dispatcher.passport_data_handler:
            self.register_passport_data_handler(dispatcher.passport_data_handler)
        if dispatcher.photo_handler:
            self.register_photo_handler(dispatcher.photo_handler)
        if dispatcher.sticker_handler:
            self.register_sticker_handler(dispatcher.sticker_handler)
        if dispatcher.successful_payment_handler:
            self.register_successful_payment_handler(dispatcher.successful_payment_handler)
        if dispatcher.venue_handler:
            self.register_venue_handler(dispatcher.venue_handler)
        if dispatcher.video_handler:
            self.register_video_handler(dispatcher.video_handler)
        if dispatcher.video_note_handler:
            self.register_video_note_handler(dispatcher.video_note_handler)
        if dispatcher.voice_handler:
            self.register_voice_handler(dispatcher.voice_handler)

    def _run_statements(self, update):
        for statement in self.statements:
            if self.success:
                break
            statement(update)

    def _run_middlewares(self, update):
        return any([m(update) for m in self.middlewares])

    @staticmethod
    def _check_function_signature(function, args_count):
        signature = inspect.getfullargspec(function)
        count = len(signature.args)
        if count != args_count:
            function_string = f"{function.__name__}({', '.join(signature.args)})"
            raise TypeError(f'{function_string} must be take {args_count} positional arguments but {count} defined')

    def handle(self, update, *args, **kwargs):
        self.success = False
        if not isinstance(update, Update):
            update = Update(**update)
        if self._run_middlewares(update):
            self.success = True
            return
        self._run_statements(update)

    def polling(self, form, tick=1.0, limit=None, timeout=None, allowed_updates=None):
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


class StateDispatcher(Dispatcher):

    def __init__(self, state_manager, key):
        super().__init__()
        self._sm = state_manager
        self.key = key
        self.states = dict()

    def register_state(self, state, dispatcher):
        assert isinstance(state, str), 'state is not a str'
        assert isinstance(dispatcher, (Dispatcher, StateDispatcher))
        self.states[state] = dispatcher

    def handle(self, update, *args, **kwargs):
        self.success = False
        if not isinstance(update, Update):
            update = Update(**update)
        if self._run_middlewares(update):
            self.success = True
            return
        states = kwargs.get('states')
        self._sm.update = update
        if self._sm.is_valid_update:
            if not states:
                states = self._sm.get_all()
            dispatcher = self.states.get(states.get(self.key))
            if dispatcher:
                dispatcher.handle(update, states=states)
                self.success = True
                self._sm.update = None
                return
        self._run_statements(update)
        self._sm.update = None
