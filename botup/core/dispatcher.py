from typing import List, Callable, Optional

from . import handlers
from .types import Update, HandleFunction, MiddlewareFunction, Context
from .exceptions import IsNotPrivateUpdate


class Dispatcher:

    def __init__(self):
        self._middlewares = list()
        self._statements = set()
        self._commands = dict()
        self._callbacks = dict()
        self._messages = dict()
        self._inlines = dict()
        self._edited_message_handler = None
        self._channel_post_handler = None
        self._chosen_inline_result_handler = None
        self._edited_channel_post_handler = None
        self._message_poll_handler = None
        self._poll_answer_handler = None
        self._pre_checkout_query_handler = None
        self._shipping_query_handler = None
        self._dice_handler = None
        self._document_handler = None
        self._animation_handler = None
        self._audio_handler = None
        self._contact_handler = None
        self._game_handler = None
        self._invoice_handler = None
        self._left_chat_member_handler = None
        self._location_handler = None
        self._new_chat_members_handler = None
        self._new_chat_photo_handler = None
        self._new_chat_title_handler = None
        self._photo_handler = None
        self._sticker_handler = None
        self._successful_payment_handler = None
        self._venue_handler = None
        self._video_handler = None
        self._video_note_handler = None
        self._voice_handler = None

    def middleware(self, function: MiddlewareFunction) -> Callable:
        self.register_middleware(function)
        return function

    def command_handler(self, command: str) -> Callable:
        def inner(handler: HandleFunction):
            self.register_command_handler(command, handler)
            return handler
        return inner

    def callback_handler(self, callback: str) -> Callable:
        def inner(handler: HandleFunction):
            self.register_callback_handler(callback, handler)
            return handler
        return inner

    def message_handler(self, message: str) -> Callable:
        def inner(handler: HandleFunction):
            self.register_message_handler(message, handler)
            return handler
        return inner

    def inline_handler(self, inline_query: str) -> Callable:
        def inner(handler: HandleFunction):
            self.register_inline_handler(inline_query, handler)
            return handler
        return inner

    def channel_post_handler(self, handler: HandleFunction):
        self.register_channel_post_handler(handler)
        return handler

    def chosen_inline_result_handler(self, handler: HandleFunction):
        self.register_chosen_inline_result_handler(handler)
        return handler

    def edited_channel_post_handler(self, handler: HandleFunction):
        self.register_edited_channel_post_handler(handler)
        return handler

    def edited_message_handler(self, handler: HandleFunction):
        self.register_edited_message_handler(handler)
        return handler

    def poll_handler(self, handler: HandleFunction):
        self.register_message_poll_handler(handler)
        return handler

    def poll_answer_handler(self, handler: HandleFunction):
        self.register_poll_answer_handler(handler)
        return handler

    def pre_checkout_query_handler(self, handler: HandleFunction):
        self.register_pre_checkout_query_handler(handler)
        return handler

    def shipping_query_handler(self, handler: HandleFunction):
        self.register_shipping_query_handler(handler)
        return handler

    def dice_handler(self, handler: HandleFunction):
        self.register_dice_handler(handler)
        return handler

    def document_handler(self, handler: HandleFunction):
        self.register_document_handler(handler)
        return handler

    def animation_handler(self, handler: HandleFunction):
        self.register_animation_handler(handler)
        return handler

    def audio_handler(self, handler: HandleFunction):
        self.register_audio_handler(handler)
        return handler

    def contact_handler(self, handler: HandleFunction):
        self.register_contact_handler(handler)
        return handler

    def game_handler(self, handler: HandleFunction):
        self.register_game_handler(handler)
        return handler

    def invoice_handler(self, handler: HandleFunction):
        self.register_invoice_handler(handler)
        return handler

    def left_chat_member_handler(self, handler: HandleFunction):
        self.register_left_chat_member_handler(handler)
        return handler

    def location_handler(self, handler: HandleFunction):
        self.register_location_handler(handler)
        return handler

    def new_chat_members_handler(self, handler: HandleFunction):
        self.register_new_chat_members_handler(handler)
        return handler

    def new_chat_photo_handler(self, handler: HandleFunction):
        self.register_new_chat_photo_handler(handler)
        return handler

    def new_chat_title_handler(self, handler: HandleFunction):
        self.register_new_chat_title_handler(handler)
        return handler

    def photo_handler(self, handler: HandleFunction):
        self.register_photo_handler(handler)
        return handler

    def sticker_handler(self, handler: HandleFunction):
        self.register_sticker_handler(handler)
        return handler

    def successful_payment_handler(self, handler: HandleFunction):
        self.register_successful_payment_handler(handler)
        return handler

    def venue_handler(self, handler: HandleFunction):
        self.register_venue_handler(handler)
        return handler

    def video_handler(self, handler: HandleFunction):
        self.register_video_handler(handler)
        return handler

    def video_note_handler(self, handler: HandleFunction):
        self.register_video_note_handler(handler)
        return handler

    def voice_handler(self, handler: HandleFunction):
        self.register_voice_handler(handler)
        return handler

    def register_middleware(self, middleware: MiddlewareFunction):
        self._middlewares.append(middleware)

    def register_command_handler(self, command: str, handler: HandleFunction):
        self._statements.add(self._is_command)
        if isinstance(command, str) and not command.startswith('/'):
            command = f'/{command}'
        self._commands[command] = handler

    def register_message_handler(self, message: str, handler: HandleFunction):
        self._statements.add(self._is_message)
        self._messages[message] = handler

    def register_callback_handler(self, callback: str, handler: HandleFunction):
        self._statements.add(self._is_callback)
        self._callbacks[callback] = handler

    def register_inline_handler(self, inline_query: str, handler: HandleFunction):
        self._statements.add(self._is_inline)
        self._inlines[inline_query] = handler

    def register_channel_post_handler(self, handler: HandleFunction):
        self._statements.add(self._is_channel_post)
        self._channel_post_handler = handler

    def register_edited_message_handler(self, handler: HandleFunction):
        self._statements.add(self._is_edited_message)
        self._edited_message_handler = handler

    def register_edited_channel_post_handler(self, handler: HandleFunction):
        self._statements.add(self._is_edited_channel_post)
        self._edited_channel_post_handler = handler

    def register_chosen_inline_result_handler(self, handler: HandleFunction):
        self._statements.add(self._is_chosen_inline_result)
        self._chosen_inline_result_handler = handler

    def register_shipping_query_handler(self, handler: HandleFunction):
        self._statements.add(self._is_shipping_query)
        self._shipping_query_handler = handler

    def register_pre_checkout_query_handler(self, handler: HandleFunction):
        self._statements.add(self._is_pre_checkout_query)
        self._pre_checkout_query_handler = handler

    def register_message_poll_handler(self, handler: HandleFunction):
        self._statements.add(self._is_message_poll)
        self._message_poll_handler = handler

    def register_poll_answer_handler(self, handler: HandleFunction):
        self._statements.add(self._is_poll_answer)
        self._poll_answer_handler = handler

    def register_dice_handler(self, handler: HandleFunction):
        self._statements.add(self._is_dice)
        self._dice_handler = handler

    def register_document_handler(self, handler: HandleFunction):
        self._statements.add(self._is_document)
        self._document_handler = handler

    def register_animation_handler(self, handler: HandleFunction):
        self._statements.add(self._is_animation)
        self._animation_handler = handler

    def register_audio_handler(self, handler: HandleFunction):
        self._statements.add(self._is_audio)
        self._audio_handler = handler

    def register_contact_handler(self, handler: HandleFunction):
        self._statements.add(self._is_contact)
        self._contact_handler = handler

    def register_game_handler(self, handler: HandleFunction):
        self._statements.add(self._is_game)
        self._game_handler = handler

    def register_invoice_handler(self, handler: HandleFunction):
        self._statements.add(self._is_invoice)
        self._invoice_handler = handler

    def register_left_chat_member_handler(self, handler: HandleFunction):
        self._statements.add(self._is_left_chat_member)
        self._left_chat_member_handler = handler

    def register_location_handler(self, handler: HandleFunction):
        self._statements.add(self._is_location)
        self._location_handler = handler

    def register_new_chat_members_handler(self, handler: HandleFunction):
        self._statements.add(self._is_new_chat_members)
        self._new_chat_members_handler = handler

    def register_new_chat_photo_handler(self, handler: HandleFunction):
        self._statements.add(self._is_new_chat_photo)
        self._new_chat_photo_handler = handler

    def register_new_chat_title_handler(self, handler):
        self._statements.add(self._is_new_chat_title)
        self._new_chat_title_handler = handler

    def register_photo_handler(self, handler: HandleFunction):
        self._statements.add(self._is_photo)
        self._photo_handler = handler

    def register_sticker_handler(self, handler: HandleFunction):
        self._statements.add(self._is_sticker)
        self._sticker_handler = handler

    def register_successful_payment_handler(self, handler: HandleFunction):
        self._statements.add(self._is_successful_payment)
        self._successful_payment_handler = handler

    def register_venue_handler(self, handler: HandleFunction):
        self._statements.add(self._is_venue)
        self._venue_handler = handler

    def register_video_handler(self, handler: HandleFunction):
        self._statements.add(self._is_video)
        self._video_handler = handler

    def register_video_note_handler(self, handler: HandleFunction):
        self._statements.add(self._is_video_note)
        self._video_note_handler = handler

    def register_voice_handler(self, handler: HandleFunction):
        self._statements.add(self._is_voice)
        self._voice_handler = handler

    async def _is_command(self, context: Context) -> bool:
        if context.is_message_command:
            return await handlers.CommandHandler.handle(context, self._commands)

    async def _is_message(self, context: Context) -> bool:
        if context.is_message_text:
            return await handlers.MessageHandler.handle(context, self._messages)

    async def _is_callback(self, context: Context) -> bool:
        if context.is_callback_query:
            return await handlers.CallbackQueryHandler.handle(context, self._callbacks)

    async def _is_inline(self, context: Context) -> bool:
        if context.is_inline_query:
            return await handlers.InlineQueryHandler.handle(context, self._inlines)

    async def _is_channel_post(self, context: Context) -> bool:
        if context.is_channel_post:
            return await handlers.ChannelPostHandler.handle(context, self._channel_post_handler)

    async def _is_edited_message(self, context: Context) -> bool:
        if context.is_edited_message:
            return await handlers.EditedMessageHandler.handle(context, self._edited_message_handler)

    async def _is_edited_channel_post(self, context: Context) -> bool:
        if context.is_edited_channel_post:
            return await handlers.EditedChannelPostHandler.handle(context, self._edited_channel_post_handler)

    async def _is_chosen_inline_result(self, context: Context) -> bool:
        if context.is_chosen_inline_query:
            return await handlers.ChosenInlineResultHandler.handle(context, self._chosen_inline_result_handler)

    async def _is_shipping_query(self, context: Context) -> bool:
        if context.is_shipping_query:
            return await handlers.ShippingQueryHandler.handle(context, self._shipping_query_handler)

    async def _is_pre_checkout_query(self, context: Context) -> bool:
        if context.is_pre_checkout_query:
            return await handlers.PreCheckoutQueryHandler.handle(context, self._pre_checkout_query_handler)

    async def _is_message_poll(self, context: Context) -> bool:
        if context.is_message_poll:
            return await handlers.MessagePollHandler.handle(context, self._message_poll_handler)

    async def _is_poll_answer(self, context: Context) -> bool:
        if context.is_poll_answer:
            return await handlers.PollAnswerHandler.handle(context, self._poll_answer_handler)

    async def _is_dice(self, context: Context) -> bool:
        if context.is_message_dice:
            return await handlers.DiceHandler.handle(context, self._dice_handler)

    async def _is_document(self, context: Context) -> bool:
        if context.is_message_document:
            return await handlers.DocumentHandler.handle(context, self._document_handler)

    async def _is_animation(self, context: Context) -> bool:
        if context.is_message_animation:
            return await handlers.AnimationHandler.handle(context, self._animation_handler)

    async def _is_audio(self, context: Context) -> bool:
        if context.is_message_audio:
            return await handlers.AudioHandler.handle(context, self._audio_handler)

    async def _is_contact(self, context: Context) -> bool:
        if context.is_message_contact:
            return await handlers.ContactHandler.handle(context, self._contact_handler)

    async def _is_game(self, context: Context) -> bool:
        if context.is_message_game:
            return await handlers.GameHandler.handle(context, self._game_handler)

    async def _is_invoice(self, context: Context) -> bool:
        if context.is_message_invoice:
            return await handlers.InvoiceHandler.handle(context, self._invoice_handler)

    async def _is_left_chat_member(self, context: Context) -> bool:
        if context.is_message_left_chat_member:
            return await handlers.LeftChatMemberHandler.handle(context, self._left_chat_member_handler)

    async def _is_location(self, context: Context) -> bool:
        if context.is_message_location:
            return await handlers.LocationHandler.handle(context, self._location_handler)

    async def _is_new_chat_members(self, context: Context) -> bool:
        if context.is_message_new_chat_members:
            return await handlers.NewChatMembersHandler.handle(context, self._new_chat_members_handler)

    async def _is_new_chat_photo(self, context: Context) -> bool:
        if context.is_message_new_chat_photo:
            return await handlers.NewChatPhotoHandler.handle(context, self._new_chat_photo_handler)

    async def _is_new_chat_title(self, context: Context) -> bool:
        if context.is_message_new_chat_title:
            return await handlers.NewChatTitleHandler.handle(context, self._new_chat_title_handler)

    async def _is_photo(self, context: Context) -> bool:
        if context.is_message_photo:
            return await handlers.PhotoHandler.handle(context, self._photo_handler)

    async def _is_sticker(self, context: Context) -> bool:
        if context.is_message_sticker:
            return await handlers.StickerHandler.handle(context, self._sticker_handler)

    async def _is_successful_payment(self, context: Context) -> bool:
        if context.is_message_successful_payment:
            return await handlers.SuccessfulPaymentHandler.handle(context, self._successful_payment_handler)

    async def _is_venue(self, context: Context) -> bool:
        if context.is_message_venue:
            return await handlers.VenueHandler.handle(context, self._venue_handler)

    async def _is_video(self, context: Context) -> bool:
        if context.is_message_video:
            return await handlers.VideoHandler.handle(context, self._video_handler)

    async def _is_video_note(self, context: Context) -> bool:
        if context.is_message_video_note:
            return await handlers.VideoNoteHandler.handle(context, self._video_note_handler)

    async def _is_voice(self, context: Context) -> bool:
        if context.is_message_voice:
            return await handlers.VoiceHandler.handle(context, self._voice_handler)

    async def _run_statements(self, context: Context) -> bool:
        for statement in self._statements:
            if await statement(context):
                return True

        return False

    async def _run_middlewares(self, context: Context) -> bool:
        for middleware in self._middlewares:
            result = await middleware(context)
            if result:
                return True

        return False

    async def handle(self, update: dict) -> bool:
        return await self._handle(Context(Update.from_dict(update)))

    async def _handle(self, context: Context, *args, **kwargs) -> bool:
        if await self._run_middlewares(context):
            return True

        return await self._run_statements(context)


class StateManager:

    def __init__(self):
        self.context: Optional[Context] = None

    def set(self, key: str, value: str) -> bool:
        raise NotImplemented

    def get_all(self) -> dict:
        raise NotImplemented

    def get(self, key: str) -> dict:
        raise NotImplemented

    def reset(self, *keys: List[str]) -> bool:
        raise NotImplemented

    def reset_all(self) -> bool:
        raise NotImplemented


class StateDispatcher(Dispatcher):

    def __init__(self, state_manager: StateManager, key: str):
        super().__init__()
        self._sm = state_manager
        self.key = key
        self._states = dict()

    def register_state(self, state: str, dispatcher: Dispatcher):
        self._states[state] = dispatcher

    def direct_handling(self, handler: HandleFunction):
        async def new_handler(context: Context):
            if self._sm.get(self.key):
                return
            await handler(context)
        return new_handler

    async def _handle(self, context: Context, *args, **kwargs):
        if await self._run_middlewares(context):
            return True

        self._sm.context = context
        states = kwargs.get('states') or self._sm.get_all()
        dispatcher = self._states.get(states.get(self.key))
        processed = False

        if dispatcher:
            processed = await dispatcher.handle(context, states=states)

        processed = processed or await self._run_statements(context)

        if processed:
            self._sm.update = None
            return True


class RedisStateManager(StateManager):

    def __init__(self, connection, name='botup:{}:state'):
        super().__init__()
        self.connection = connection
        self.name = name

    def set(self, key: str, value: str):
        if not self.context.is_private_update:
            raise IsNotPrivateUpdate

        return self.connection.hset(self.name.format(self.context.chat_id), key, value)

    def get_all(self):
        if not self.context.is_private_update:
            raise IsNotPrivateUpdate

        return self.connection.hgetall(self.name.format(self.context.chat_id))

    def get(self, key: str):
        if not self.context.is_private_update:
            raise IsNotPrivateUpdate

        return self.connection.hget(self.name.format(self.context.chat_id), key)

    def reset(self, *keys: List[str]):
        if not self.context.is_private_update:
            raise IsNotPrivateUpdate

        return self.connection.hdel(self.name.format(self.context.chat_id), *keys)

    def reset_all(self):
        if not self.context.is_private_update:
            raise IsNotPrivateUpdate

        return self.connection.delete(self.name.format(self.context.chat_id))


class DictStateManager(StateManager):
    def __init__(self):
        super().__init__()
        self._data = dict()

    def set(self, key: str, value: str):
        if not self.context.is_private_update:
            raise IsNotPrivateUpdate

        user_dict = self._data.setdefault(str(self.context.chat_id), {})
        user_dict[key] = value
        return True

    def get_all(self):
        if not self.context.is_private_update:
            raise IsNotPrivateUpdate

        user_dict = self._data.setdefault(str(self.context.chat_id), {})
        return user_dict

    def get(self, key: str):
        if not self.context.is_private_update:
            raise IsNotPrivateUpdate

        user_dict = self._data.setdefault(str(self.context.chat_id), {})
        return user_dict.get(key)

    def reset(self, *keys: List[str]):
        if not self.context.is_private_update:
            raise IsNotPrivateUpdate

        user_dict = self._data.setdefault(str(self.context.chat_id), {})
        for k in keys:
            try:
                user_dict.pop(k)
            except KeyError:
                pass
        return True

    def reset_all(self):
        if not self.context.is_private_update:
            raise IsNotPrivateUpdate

        self._data.setdefault(str(self.context.chat_id), {})
        del self._data[str(self.context.chat_id)]
