import threading
import inspect

try:
    import ujson as json
except ImportError:
    import json

from . import handlers
from .types import Update
from .exceptions import StateManagerException


class Dispatcher:

    def __init__(self):
        self._success = False
        self._middlewares = list()
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

    def register_middleware(self, middleware):
        self._check_function_signature(middleware, 1)
        self._middlewares.append(middleware)

    def register_command_handler(self, command, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_command)
        if isinstance(command, str) and not command.startswith('/'):
            command = f'/{command}'
        self._commands[command] = handler

    def register_message_handler(self, message, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_message)
        self._messages[message] = handler

    def register_callback_handler(self, callback, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_callback)
        self._callbacks[callback] = handler

    def register_inline_handler(self, inline_query, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_inline)
        self._inlines[inline_query] = handler

    def register_channel_post_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_channel_post)
        self._channel_post_handler = handler

    def register_edited_message_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_edited_message)
        self._edited_message_handler = handler

    def register_edited_channel_post_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_edited_channel_post)
        self._edited_channel_post_handler = handler

    def register_chosen_inline_result_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_chosen_inline_result)
        self._chosen_inline_result_handler = handler

    def register_shipping_query_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_shipping_query)
        self._shipping_query_handler = handler

    def register_pre_checkout_query_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_pre_checkout_query)
        self._pre_checkout_query_handler = handler

    def register_poll_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_poll)
        self._poll_handler = handler

    def register_document_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_document)
        self._document_handler = handler

    def register_animation_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_animation)
        self._animation_handler = handler

    def register_audio_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_audio)
        self._audio_handler = handler

    def register_connected_website_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_connected_website)
        self._connected_website_handler = handler

    def register_contact_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_contact)
        self._contact_handler = handler

    def register_game_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_game)
        self._game_handler = handler

    def register_invoice_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_invoice)
        self._invoice_handler = handler

    def register_left_chat_member_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_left_chat_member)
        self._left_chat_member_handler = handler

    def register_location_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_location)
        self._location_handler = handler

    def register_new_chat_members_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_new_chat_members)
        self._new_chat_members_handler = handler

    def register_new_chat_photo_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_new_chat_photo)
        self._new_chat_photo_handler = handler

    def register_new_chat_title_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_new_chat_title)
        self._new_chat_title_handler = handler

    def register_passport_data_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_passport_data)
        self._passport_data_handler = handler

    def register_photo_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_photo)
        self._photo_handler = handler

    def register_sticker_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_sticker)
        self._sticker_handler = handler

    def register_successful_payment_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_successful_payment)
        self._successful_payment_handler = handler

    def register_venue_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_venue)
        self._venue_handler = handler

    def register_video_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_video)
        self._video_handler = handler

    def register_video_note_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_video_note)
        self._video_note_handler = handler

    def register_voice_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_voice)
        self._voice_handler = handler

    def _is_command(self, update):
        if update.message and update.message.text and update.message.text.startswith('/'):
            self._success = True
            handlers.CommandHandler(update, self._commands).handle()

    def _is_message(self, update):
        if update.message and update.message.text and not update.message.text.startswith('/'):
            self._success = True
            handlers.MessageHandler(update, self._messages).handle()

    def _is_callback(self, update):
        if update.callback_query:
            self._success = True
            handlers.CallbackQueryHandler(update, self._callbacks).handle()

    def _is_inline(self, update):
        if update.inline_query:
            self._success = True
            handlers.InlineQueryHandler(update, self._inlines).handle()

    def _is_channel_post(self, update):
        if update.channel_post:
            self._success = True
            handlers.ChannelPostHandler(update, self._channel_post_handler).handle()

    def _is_edited_message(self, update):
        if update.edited_message:
            self._success = True
            handlers.EditedMessageHandler(update, self._edited_message_handler).handle()

    def _is_edited_channel_post(self, update):
        if update.edited_channel_post:
            self._success = True
            handlers.EditedChannelPostHandler(update, self._edited_channel_post_handler).handle()

    def _is_chosen_inline_result(self, update):
        if update.chosen_inline_result:
            self._success = True
            handlers.ChosenInlineResultHandler(update, self._chosen_inline_result_handler).handle()

    def _is_shipping_query(self, update):
        if update.shipping_query:
            self._success = True
            handlers.ShippingQueryHandler(update, self._shipping_query_handler).handle()

    def _is_pre_checkout_query(self, update):
        if update.pre_checkout_query:
            self._success = True
            handlers.PreCheckoutQueryHandler(update, self._pre_checkout_query_handler).handle()

    def _is_poll(self, update):
        if update.poll:
            self._success = True
            handlers.PollHandler(update, self._poll_handler).handle()

    def _is_document(self, update):
        if update.message and update.message.document and not update.message.animation:
            self._success = True
            handlers.DocumentHandler(update, self._document_handler).handle()

    def _is_animation(self, update):
        if update.message and update.message.animation:
            self._success = True
            handlers.AnimationHandler(update, self._animation_handler).handle()

    def _is_audio(self, update):
        if update.message and update.message.audio:
            self._success = True
            handlers.AudioHandler(update, self._audio_handler).handle()

    def _is_connected_website(self, update):
        if update.message and update.message.connected_website:
            self._success = True
            handlers.ConnectedWebsiteHandler(update, self._connected_website_handler).handle()

    def _is_contact(self, update):
        if update.message and update.message.contact:
            self._success = True
            handlers.ContactHandler(update, self._contact_handler).handle()

    def _is_game(self, update):
        if update.message and update.message.game:
            self._success = True
            handlers.GameHandler(update, self._game_handler).handle()

    def _is_invoice(self, update):
        if update.message and update.message.invoice:
            self._success = True
            handlers.InvoiceHandler(update, self._invoice_handler).handle()

    def _is_left_chat_member(self, update):
        if update.message and update.message.left_chat_member:
            self._success = True
            handlers.LeftChatMemberHandler(update, self._left_chat_member_handler).handle()

    def _is_location(self, update):
        if update.message and update.message.location:
            self._success = True
            handlers.LocationHandler(update, self._location_handler).handle()

    def _is_new_chat_members(self, update):
        if update.message and update.message.new_chat_members:
            self._success = True
            handlers.NewChatMembersHandler(update, self._new_chat_members_handler).handle()

    def _is_new_chat_photo(self, update):
        if update.message and update.message.new_chat_photo:
            self._success = True
            handlers.NewChatPhotoHandler(update, self._new_chat_photo_handler).handle()

    def _is_new_chat_title(self, update):
        if update.message and update.message.new_chat_title:
            self._success = True
            handlers.NewChatTitleHandler(update, self._new_chat_title_handler).handle()

    def _is_passport_data(self, update):
        if update.message and update.message.passport_data:
            self._success = True
            handlers.PassportDataHandler(update, self._passport_data_handler).handle()

    def _is_photo(self, update):
        if update.message and update.message.photo:
            self._success = True
            handlers.PhotoHandler(update, self._photo_handler).handle()

    def _is_sticker(self, update):
        if update.message and update.message.sticker:
            self._success = True
            handlers.StickerHandler(update, self._sticker_handler).handle()

    def _is_successful_payment(self, update):
        if update.message and update.message.successful_payment:
            self._success = True
            handlers.SuccessfulPaymentHandler(update, self._successful_payment_handler).handle()

    def _is_venue(self, update):
        if update.message and update.message.venue:
            self._success = True
            handlers.VenueHandler(update, self._venue_handler).handle()

    def _is_video(self, update):
        if update.message and update.message.video:
            self._success = True
            handlers.VideoHandler(update, self._video_handler).handle()

    def _is_video_note(self, update):
        if update.message and update.message.video_note:
            self._success = True
            handlers.VideoNoteHandler(update, self._video_note_handler).handle()

    def _is_voice(self, update):
        if update.message and update.message.voice:
            self._success = True
            handlers.VoiceHandler(update, self._voice_handler).handle()

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
        for statement in self._statements:
            if self._success:
                break
            statement(update)

    def _run_middlewares(self, update):
        return any([m(update) for m in self._middlewares])

    @staticmethod
    def _check_function_signature(function, args_count):
        signature = inspect.getfullargspec(function)
        count = len(signature.args)
        if count != args_count:
            function_string = f"{function.__name__}({', '.join(signature.args)})"
            raise TypeError(f'{function_string} must be take {args_count} positional arguments but {count} defined')

    def handle(self, update, *args, **kwargs):
        self._success = False
        if not isinstance(update, Update):
            update = Update(**update)
        if self._run_middlewares(update):
            self._success = True
            return
        self._run_statements(update)

    def polling(self, sender, tick=1.0, limit=None, timeout=None, allowed_updates=None):
        last_update_id = 0
        response = sender.get_updates(limit=limit, timeout=timeout, allowed_updates=allowed_updates)
        while True:
            response = json.loads(response)
            for update in response['result']:
                last_update_id = update['update_id']
                self.handle(update)
            timer = threading.Timer(tick, lambda *args: None)
            timer.start()
            timer.join()
            response = sender.get_updates(
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
        self._states = dict()

    def register_state(self, state, dispatcher):
        assert isinstance(state, str), 'state is not a str'
        assert isinstance(dispatcher, (Dispatcher, StateDispatcher))
        self._states[state] = dispatcher

    def handle(self, update, *args, **kwargs):
        self._success = False
        if not isinstance(update, Update):
            update = Update(**update)
        if self._run_middlewares(update):
            self._success = True
            return
        states = kwargs.get('states')
        self._sm.update = update
        if self._sm.is_valid_update:
            if not states:
                states = self._sm.get_all()
            dispatcher = self._states.get(states.get(self.key))
            if dispatcher:
                dispatcher.handle(update, states=states)
                self._success = True
                self._sm.update = None
                return
        self._run_statements(update)
        self._sm.update = None


class StateManager:

    def __init__(self, connection, name='botup:{}:state'):
        self.connection = connection
        self.name = name
        self.update = None

    def set(self, key, value):
        message = self.update.message or getattr(self.update.callback_query, 'message', None)
        if not message:
            raise StateManagerException(f'Cannot set state with {self.update.pformat()}')
        return self.connection.hset(self.name.format(message.chat.id), key, value)

    def get_all(self):
        message = self.update.message or getattr(self.update.callback_query, 'message', None)
        if not message:
            raise StateManagerException(f'Cannot get state with {self.update.pformat()}')
        return self.connection.hgetall(self.name.format(message.chat.id))

    def get(self, key):
        message = self.update.message or getattr(self.update.callback_query, 'message', None)
        if not message:
            raise StateManagerException(f'Cannot get state with {self.update.pformat()}')
        return self.connection.hgetall(self.name.format(message.chat.id), key)

    def reset(self, *keys):
        message = self.update.message or getattr(self.update.callback_query, 'message', None)
        if not message:
            raise StateManagerException(f'Cannot delete state with {self.update.pformat()}')
        return self.connection.hdel(self.name.format(message.chat.id), *keys)

    @property
    def is_valid_update(self):
        return self.update.message or getattr(self.update.callback_query, 'message', None) is not None
