import inspect

import typing

try:
    import ujson as json
except ImportError:
    import json

from . import handlers
from .utils import get_chat_id
from .types import Update
from .exceptions import StateManagerException, BadHandlerException


class Dispatcher:

    def __init__(self):
        self._success = False
        self._registration_map = {
            handlers.AnimationHandler: self.register_animation_handler,
            handlers.AudioHandler: self.register_audio_handler,
            handlers.CallbackQueryHandler: self.register_callback_handler,
            handlers.ChannelPostHandler: self.register_channel_post_handler,
            handlers.ChosenInlineResultHandler: self.register_chosen_inline_result_handler,
            handlers.CommandHandler: self.register_command_handler,
            handlers.ConnectedWebsiteHandler: self.register_connected_website_handler,
            handlers.ContactHandler: self.register_contact_handler,
            handlers.DiceHandler: self.register_dice_handler,
            handlers.DocumentHandler: self.register_document_handler,
            handlers.EditedChannelPostHandler: self.register_edited_channel_post_handler,
            handlers.EditedMessageHandler: self.register_edited_message_handler,
            handlers.GameHandler: self.register_game_handler,
            handlers.InlineQueryHandler: self.register_inline_handler,
            handlers.InvoiceHandler: self.register_invoice_handler,
            handlers.LeftChatMemberHandler: self.register_left_chat_member_handler,
            handlers.LocationHandler: self.register_location_handler,
            handlers.MessageHandler: self.register_message_handler,
            handlers.NewChatMembersHandler: self.register_new_chat_members_handler,
            handlers.NewChatPhotoHandler: self.register_new_chat_photo_handler,
            handlers.NewChatTitleHandler: self.register_new_chat_title_handler,
            handlers.PassportDataHandler: self.register_passport_data_handler,
            handlers.PhotoHandler: self.register_photo_handler,
            handlers.PollHandler: self.register_poll_handler,
            handlers.PollAnswerHandler: self.register_poll_answer_handler,
            handlers.PreCheckoutQueryHandler: self.register_pre_checkout_query_handler,
            handlers.ShippingQueryHandler: self.register_shipping_query_handler,
            handlers.StickerHandler: self.register_sticker_handler,
            handlers.SuccessfulPaymentHandler: self.register_successful_payment_handler,
            handlers.VenueHandler: self.register_venue_handler,
            handlers.VideoHandler: self.register_video_handler,
            handlers.VideoNoteHandler: self.register_video_note_handler,
            handlers.VoiceHandler: self.register_voice_handler
        }
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
        self._poll_answer_handler = None
        self._pre_checkout_query_handler = None
        self._shipping_query_handler = None
        self._dice_handler = None
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

    def register(self, handler):
        handler_type = type(handler)
        if handler_type not in self._registration_map:
            raise BadHandlerException(f'Bad  handler {handler}')
        args = (handler.pattern, handler.function) if hasattr(handler, 'pattern') else (handler.function,)
        registration_method = self._registration_map[handler_type]
        registration_method(*args)

    def middleware(self, function):
        self.register_middleware(function)
        return function

    def command_handler(self, command):
        def inner(handler):
            self.register_command_handler(command, handler)
            return handler
        return inner

    def callback_handler(self, callback):
        def inner(handler):
            self.register_callback_handler(callback, handler)
            return handler
        return inner

    def message_handler(self, message):
        def inner(handler):
            self.register_message_handler(message, handler)
            return handler
        return inner

    def inline_handler(self, inline_query):
        def inner(handler):
            self.register_inline_handler(inline_query, handler)
            return handler
        return inner

    def channel_post_handler(self, handler):
        self.register_channel_post_handler(handler)
        return handler

    def chosen_inline_result_handler(self, handler):
        self.register_chosen_inline_result_handler(handler)
        return handler

    def edited_channel_post_handler(self, handler):
        self.register_edited_channel_post_handler(handler)
        return handler

    def edited_message_handler(self, handler):
        self.register_edited_message_handler(handler)
        return handler

    def poll_handler(self, handler):
        self.register_poll_handler(handler)
        return handler

    def poll_answer_handler(self, handler):
        self.register_poll_answer_handler(handler)
        return handler

    def pre_checkout_query_handler(self, handler):
        self.register_pre_checkout_query_handler(handler)
        return handler

    def shipping_query_handler(self, handler):
        self.register_shipping_query_handler(handler)
        return handler

    def dice_handler(self, handler):
        self.register_dice_handler(handler)
        return handler

    def document_handler(self, handler):
        self.register_document_handler(handler)
        return handler

    def animation_handler(self, handler):
        self.register_animation_handler(handler)
        return handler

    def audio_handler(self, handler):
        self.register_audio_handler(handler)
        return handler

    def connected_website_handler(self, handler):
        self.register_connected_website_handler(handler)
        return handler

    def contact_handler(self, handler):
        self.register_contact_handler(handler)
        return handler

    def game_handler(self, handler):
        self.register_game_handler(handler)
        return handler

    def invoice_handler(self, handler):
        self.register_invoice_handler(handler)
        return handler

    def left_chat_member_handler(self, handler):
        self.register_left_chat_member_handler(handler)
        return handler

    def location_handler(self, handler):
        self.register_location_handler(handler)
        return handler

    def new_chat_members_handler(self, handler):
        self.register_new_chat_members_handler(handler)
        return handler

    def new_chat_photo_handler(self, handler):
        self.register_new_chat_photo_handler(handler)
        return handler

    def new_chat_title_handler(self, handler):
        self.register_new_chat_title_handler(handler)
        return handler

    def passport_data_handler(self, handler):
        self.register_passport_data_handler(handler)
        return handler

    def photo_handler(self, handler):
        self.register_photo_handler(handler)
        return handler

    def sticker_handler(self, handler):
        self.register_sticker_handler(handler)
        return handler

    def successful_payment_handler(self, handler):
        self.register_successful_payment_handler(handler)
        return handler

    def venue_handler(self, handler):
        self.register_venue_handler(handler)
        return handler

    def video_handler(self, handler):
        self.register_video_handler(handler)
        return handler

    def video_note_handler(self, handler):
        self.register_video_note_handler(handler)
        return handler

    def voice_handler(self, handler):
        self.register_voice_handler(handler)
        return handler

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

    def register_poll_answer_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_poll_answer)
        self._poll_answer_handler = handler

    def register_dice_handler(self, handler):
        self._check_function_signature(handler, 2)
        self._statements.add(self._is_dice)
        self._dice_handler = handler

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

    async def _is_command(self, update):
        if update.message and update.message.text and update.message.text.startswith('/'):
            self._success = True
            return await handlers.CommandHandler.handle(update, self._commands)

    async def _is_message(self, update):
        if update.message and update.message.text and not update.message.text.startswith('/'):
            return await handlers.MessageHandler.handle(update, self._messages)

    async def _is_callback(self, update):
        if update.callback_query:
            return await handlers.CallbackQueryHandler.handle(update, self._callbacks)

    async def _is_inline(self, update):
        if update.inline_query:
            return await handlers.InlineQueryHandler.handle(update, self._inlines)

    async def _is_channel_post(self, update):
        if update.channel_post:
            return await handlers.ChannelPostHandler.handle(update, self._channel_post_handler)

    async def _is_edited_message(self, update):
        if update.edited_message:
            return await handlers.EditedMessageHandler.handle(update, self._edited_message_handler)

    async def _is_edited_channel_post(self, update):
        if update.edited_channel_post:
            return await handlers.EditedChannelPostHandler.handle(update, self._edited_channel_post_handler)

    async def _is_chosen_inline_result(self, update):
        if update.chosen_inline_result:
            return await handlers.ChosenInlineResultHandler.handle(update, self._chosen_inline_result_handler)

    async def _is_shipping_query(self, update):
        if update.shipping_query:
            return await handlers.ShippingQueryHandler.handle(update, self._shipping_query_handler)

    async def _is_pre_checkout_query(self, update):
        if update.pre_checkout_query:
            return await handlers.PreCheckoutQueryHandler.handle(update, self._pre_checkout_query_handler)

    async def _is_poll(self, update):
        if update.poll:
            return await handlers.PollHandler.handle(update, self._poll_handler)

    async def _is_poll_answer(self, update):
        if update.poll_answer:
            return await handlers.PollAnswerHandler.handle(update, self._poll_answer_handler)

    async def _is_dice(self, update):
        if update.message and update.message.dice:
            return await handlers.DiceHandler.handle(update, self._dice_handler)

    async def _is_document(self, update):
        if update.message and update.message.document and not update.message.animation:
            return await handlers.DocumentHandler.handle(update, self._document_handler)

    async def _is_animation(self, update):
        if update.message and update.message.animation:
            return await handlers.AnimationHandler.handle(update, self._animation_handler)

    async def _is_audio(self, update):
        if update.message and update.message.audio:
            return await handlers.AudioHandler.handle(update, self._audio_handler)

    async def _is_connected_website(self, update):
        if update.message and update.message.connected_website:
            return await handlers.ConnectedWebsiteHandler.handle(update, self._connected_website_handler)

    async def _is_contact(self, update):
        if update.message and update.message.contact:
            return await handlers.ContactHandler.handle(update, self._contact_handler)

    async def _is_game(self, update):
        if update.message and update.message.game:
            return await handlers.GameHandler.handle(update, self._game_handler)

    async def _is_invoice(self, update):
        if update.message and update.message.invoice:
            return await handlers.InvoiceHandler.handle(update, self._invoice_handler)

    async def _is_left_chat_member(self, update):
        if update.message and update.message.left_chat_member:
            return await handlers.LeftChatMemberHandler.handle(update, self._left_chat_member_handler)

    async def _is_location(self, update):
        if update.message and update.message.location:
            return await handlers.LocationHandler.handle(update, self._location_handler)

    async def _is_new_chat_members(self, update):
        if update.message and update.message.new_chat_members:
            return await handlers.NewChatMembersHandler.handle(update, self._new_chat_members_handler)

    async def _is_new_chat_photo(self, update):
        if update.message and update.message.new_chat_photo:
            return await handlers.NewChatPhotoHandler.handle(update, self._new_chat_photo_handler)

    async def _is_new_chat_title(self, update):
        if update.message and update.message.new_chat_title:
            return await handlers.NewChatTitleHandler.handle(update, self._new_chat_title_handler)

    async def _is_passport_data(self, update):
        if update.message and update.message.passport_data:
            return await handlers.PassportDataHandler.handle(update, self._passport_data_handler)

    async def _is_photo(self, update):
        if update.message and update.message.photo:
            return await handlers.PhotoHandler.handle(update, self._photo_handler)

    async def _is_sticker(self, update):
        if update.message and update.message.sticker:
            return await handlers.StickerHandler.handle(update, self._sticker_handler)

    async def _is_successful_payment(self, update):
        if update.message and update.message.successful_payment:
            return await handlers.SuccessfulPaymentHandler.handle(update, self._successful_payment_handler)

    async def _is_venue(self, update):
        if update.message and update.message.venue:
            return await handlers.VenueHandler.handle(update, self._venue_handler)

    async def _is_video(self, update):
        if update.message and update.message.video:
            return await handlers.VideoHandler.handle(update, self._video_handler)

    async def _is_video_note(self, update):
        if update.message and update.message.video_note:
            return await handlers.VideoNoteHandler.handle(update, self._video_note_handler)

    async def _is_voice(self, update):
        if update.message and update.message.voice:
            return await handlers.VoiceHandler.handle(update, self._voice_handler)

    async def _run_statements(self, update):
        for statement in self._statements:
            if await statement(update):
                return True

    async def _run_middlewares(self, update):
        for middleware in self._middlewares:
            result = await middleware(update)
            if result is True:
                return True
        return False

    @staticmethod
    def _check_function_signature(function, args_count):
        signature = inspect.getfullargspec(function)
        count = len(signature.args)
        if count != args_count:
            function_string = f"{function.__name__}({', '.join(signature.args)})"
            raise BadHandlerException(
                f'{function_string} must be take {args_count} positional arguments but {count} defined')

    async def handle(self, update, *args, **kwargs):
        if not isinstance(update, Update):
            update = Update(**update)
        if await self._run_middlewares(update):
            return True
        return await self._run_statements(update)


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

    def direct_handling(self, handler):
        async def new_handler(chat_id, update):
            if self._sm.get(self.key):
                return
            await handler(chat_id, update)
        return new_handler

    async def handle(self, update, *args, **kwargs):
        if not isinstance(update, Update):
            update = Update(**update)
        if await self._run_middlewares(update):
            return True
        self._sm.update = update
        states = kwargs.get('states') or self._sm.get_all()
        dispatcher = self._states.get(states.get(self.key))
        processed = False
        if dispatcher:
            processed = await dispatcher.handle(update, states=states)
        processed = processed or await self._run_statements(update)
        if processed:
            self._sm.update = None
            return True


class StateManager:
    def __init__(self):
        self.update = None

    def set(self, key: str, value: str) -> bool:
        raise NotImplemented

    def get_all(self) -> dict:
        raise NotImplemented

    def get(self, key: str) -> dict:
        raise NotImplemented

    def reset(self, *keys: typing.List[str]) -> bool:
        raise NotImplemented

    def reset_all(self) -> bool:
        raise NotImplemented


class RedisStateManager(StateManager):

    def __init__(self, connection, name='botup:{}:state'):
        super().__init__()
        self.connection = connection
        self.name = name

    def set(self, key, value):
        chat_id = get_chat_id(self.update)
        if not chat_id:
            raise StateManagerException(f'Cannot set state with {self.update.pformat()}')
        return self.connection.hset(self.name.format(chat_id), key, value)

    def get_all(self):
        chat_id = get_chat_id(self.update)
        if not chat_id:
            raise StateManagerException(f'Cannot get state with {self.update.pformat()}')
        return self.connection.hgetall(self.name.format(chat_id))

    def get(self, key):
        chat_id = get_chat_id(self.update)
        if not chat_id:
            raise StateManagerException(f'Cannot get state with {self.update.pformat()}')
        return self.connection.hget(self.name.format(chat_id), key)

    def reset(self, *keys):
        chat_id = get_chat_id(self.update)
        if not chat_id:
            raise StateManagerException(f'Cannot reset state with {self.update.pformat()}')
        return self.connection.hdel(self.name.format(chat_id), *keys)

    def reset_all(self):
        chat_id = get_chat_id(self.update)
        if not chat_id:
            raise StateManagerException(f'Cannot reset state with {self.update.pformat()}')
        return self.connection.delete(self.name.format(chat_id))


class DictStateManager(StateManager):
    def __init__(self):
        super().__init__()
        self._data = dict()

    def set(self, key, value):
        chat_id = get_chat_id(self.update)
        if not chat_id:
            raise StateManagerException(f'Cannot set state with {self.update.pformat()}')
        user_dict = self._data.setdefault(str(chat_id), {})
        user_dict[key] = value
        return True

    def get_all(self):
        chat_id = get_chat_id(self.update)
        if not chat_id:
            raise StateManagerException(f'Cannot get state with {self.update.pformat()}')
        user_dict = self._data.setdefault(str(chat_id), {})
        return user_dict

    def get(self, key):
        chat_id = get_chat_id(self.update)
        if not chat_id:
            raise StateManagerException(f'Cannot get state with {self.update.pformat()}')
        user_dict = self._data.setdefault(str(chat_id), {})
        return user_dict.get(key)

    def reset(self, *keys):
        chat_id = get_chat_id(self.update)
        if not chat_id:
            raise StateManagerException(f'Cannot reset state with {self.update.pformat()}')
        user_dict = self._data.setdefault(str(chat_id), {})
        for k in keys:
            try:
                user_dict.pop(k)
            except KeyError:
                pass
        return True

    def reset_all(self):
        chat_id = get_chat_id(self.update)
        if not chat_id:
            raise StateManagerException(f'Cannot reset state with {self.update.pformat()}')
        self._data.setdefault(str(chat_id), {})
        del self._data[str(chat_id)]
