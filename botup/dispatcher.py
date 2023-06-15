from typing import Callable, Pattern, Union, List

from botup.constants.update_type import (
    UpdateType,
    CALLBACK_QUERY,
    INLINE_QUERY,
    CHANNEL_POST,
    EDITED_MESSAGE,
    EDITED_CHANNEL_POST,
    CHOSEN_INLINE_RESULT,
    SHIPPING_QUERY,
    PRE_CHECKOUT_QUERY,
    POLL,
    POLL_ANSWER,
    MESSAGE_POLL,
    MESSAGE_COMMAND,
    MESSAGE_TEXT,
    MESSAGE_DICE,
    MESSAGE_DOCUMENT,
    MESSAGE_ANIMATION,
    MESSAGE_AUDIO,
    MESSAGE_CONTACT,
    MESSAGE_GAME,
    MESSAGE_INVOICE,
    MESSAGE_LEFT_CHAT_MEMBER,
    MESSAGE_LOCATION,
    MESSAGE_NEW_CHAT_MEMBERS,
    MESSAGE_NEW_CHAT_PHOTO,
    MESSAGE_NEW_CHAT_TITLE,
    MESSAGE_PHOTO,
    MESSAGE_STICKER,
    MESSAGE_SUCCESSFUL_PAYMENT,
    MESSAGE_VENUE,
    MESSAGE_VIDEO,
    MESSAGE_VIDEO_NOTE,
    MESSAGE_VOICE
)
from botup.handlers import (
    MessageCommandHandler,
    CallbackQueryHandler,
    MessageTextHandler,
    InlineQueryHandler,
    EditedMessageHandler,
    ChannelPostHandler,
    ChosenInlineResultHandler,
    EditedChannelPostHandler,
    MessagePollHandler,
    PollHandler,
    PollAnswerHandler,
    PreCheckoutQueryHandler,
    ShippingQueryHandler,
    MessageDiceHandler,
    MessageDocumentHandler,
    MessageAnimationHandler,
    MessageAudioHandler,
    MessageContactHandler,
    MessageGameHandler,
    MessageInvoiceHandler,
    MessageLeftChatMemberHandler,
    MessageLocationHandler,
    MessageNewChatMembersHandler,
    MessageNewChatPhotoHandler,
    MessageNewChatTitleHandler,
    MessagePhotoHandler,
    MessageStickerHandler,
    MessageSuccessfulPaymentHandler,
    MessageVenueHandler,
    MessageVideoHandler,
    MessageVideoNoteHandler,
    MessageVoiceHandler
)
from botup.types import Update, HandleFunction, MiddlewareFunction, BaseContext


class Dispatcher:

    def __init__(self):
        self._middlewares: List[MiddlewareFunction] = list()
        self._update_types: List[UpdateType] = list()
        self._message_command_handler = MessageCommandHandler()
        self._callback_query_handler = CallbackQueryHandler()
        self._message_text_handler = MessageTextHandler()
        self._inline_query_handler = InlineQueryHandler()
        self._edited_message_handler = EditedMessageHandler()
        self._channel_post_handler = ChannelPostHandler()
        self._chosen_inline_result_handler = ChosenInlineResultHandler()
        self._edited_channel_post_handler = EditedChannelPostHandler()
        self._message_poll_handler = MessagePollHandler()
        self._poll_handler = PollHandler()
        self._poll_answer_handler = PollAnswerHandler()
        self._pre_checkout_query_handler = PreCheckoutQueryHandler()
        self._shipping_query_handler = ShippingQueryHandler()
        self._message_dice_handler = MessageDiceHandler()
        self._message_document_handler = MessageDocumentHandler()
        self._message_animation_handler = MessageAnimationHandler()
        self._message_audio_handler = MessageAudioHandler()
        self._message_contact_handler = MessageContactHandler()
        self._message_game_handler = MessageGameHandler()
        self._message_invoice_handler = MessageInvoiceHandler()
        self._message_left_chat_member_handler = MessageLeftChatMemberHandler()
        self._message_location_handler = MessageLocationHandler()
        self._message_new_chat_members_handler = MessageNewChatMembersHandler()
        self._message_new_chat_photo_handler = MessageNewChatPhotoHandler()
        self._message_new_chat_title_handler = MessageNewChatTitleHandler()
        self._message_photo_handler = MessagePhotoHandler()
        self._message_sticker_handler = MessageStickerHandler()
        self._message_successful_payment_handler = MessageSuccessfulPaymentHandler()
        self._message_venue_handler = MessageVenueHandler()
        self._message_video_handler = MessageVideoHandler()
        self._message_video_note_handler = MessageVideoNoteHandler()
        self._message_voice_handler = MessageVoiceHandler()

    def middleware(self, function: MiddlewareFunction) -> Callable:
        self.register_middleware(function)
        return function

    def command_handler(self, command: Union[str, Pattern]) -> Callable:
        def inner(handler: HandleFunction):
            self.register_command_handler(command, handler)
            return handler

        return inner

    def callback_handler(self, callback: Union[str, Pattern]) -> Callable:
        def inner(handler: HandleFunction):
            self.register_callback_handler(callback, handler)
            return handler

        return inner

    def message_handler(self, message: Union[str, Pattern]) -> Callable:
        def inner(handler: HandleFunction):
            self.register_message_handler(message, handler)
            return handler

        return inner

    def inline_handler(self, inline_query: Union[str, Pattern]) -> Callable:
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
        self.register_poll_handler(handler)
        return handler

    def message_poll_handler(self, handler: HandleFunction):
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

    def register_command_handler(self, command: Union[str, Pattern], handler: HandleFunction):
        if MESSAGE_COMMAND not in self._update_types:
            self._update_types.append(MESSAGE_COMMAND)
        if isinstance(command, str) and not command.startswith('/'):
            command = f'/{command}'
        self._message_command_handler.register(command, handler)

    def register_message_handler(self, message: Union[str, Pattern], handler: HandleFunction):
        if MESSAGE_TEXT not in self._update_types:
            self._update_types.append(MESSAGE_TEXT)
        self._message_text_handler.register(message, handler)

    def register_callback_handler(self, callback: Union[str, Pattern], handler: HandleFunction):
        if CALLBACK_QUERY not in self._update_types:
            self._update_types.append(CALLBACK_QUERY)
        self._callback_query_handler.register(callback, handler)

    def register_inline_handler(self, inline_query: Union[str, Pattern], handler: HandleFunction):
        if INLINE_QUERY not in self._update_types:
            self._update_types.append(INLINE_QUERY)
        self._inline_query_handler.register(inline_query, handler)

    def register_channel_post_handler(self, handler: HandleFunction):
        if CHANNEL_POST not in self._update_types:
            self._update_types.append(CHANNEL_POST)
        self._channel_post_handler.register(handler)

    def register_edited_message_handler(self, handler: HandleFunction):
        if EDITED_MESSAGE not in self._update_types:
            self._update_types.append(EDITED_MESSAGE)
        self._edited_message_handler.register(handler)

    def register_edited_channel_post_handler(self, handler: HandleFunction):
        if EDITED_CHANNEL_POST not in self._update_types:
            self._update_types.append(EDITED_CHANNEL_POST)
        self._edited_channel_post_handler.register(handler)

    def register_chosen_inline_result_handler(self, handler: HandleFunction):
        if CHOSEN_INLINE_RESULT not in self._update_types:
            self._update_types.append(CHOSEN_INLINE_RESULT)
        self._chosen_inline_result_handler.register(handler)

    def register_shipping_query_handler(self, handler: HandleFunction):
        if SHIPPING_QUERY not in self._update_types:
            self._update_types.append(SHIPPING_QUERY)
        self._shipping_query_handler.register(handler)

    def register_pre_checkout_query_handler(self, handler: HandleFunction):
        if PRE_CHECKOUT_QUERY not in self._update_types:
            self._update_types.append(PRE_CHECKOUT_QUERY)
        self._pre_checkout_query_handler.register(handler)

    def register_poll_handler(self, handler: HandleFunction):
        if POLL not in self._update_types:
            self._update_types.append(POLL)
        self._poll_handler.register(handler)

    def register_message_poll_handler(self, handler: HandleFunction):
        if MESSAGE_POLL not in self._update_types:
            self._update_types.append(MESSAGE_POLL)
        self._message_poll_handler.register(handler)

    def register_poll_answer_handler(self, handler: HandleFunction):
        if POLL_ANSWER not in self._update_types:
            self._update_types.append(POLL_ANSWER)
        self._poll_answer_handler.register(handler)

    def register_dice_handler(self, handler: HandleFunction):
        if MESSAGE_DICE not in self._update_types:
            self._update_types.append(MESSAGE_DICE)
        self._message_dice_handler.register(handler)

    def register_document_handler(self, handler: HandleFunction):
        if MESSAGE_DOCUMENT not in self._update_types:
            self._update_types.append(MESSAGE_DOCUMENT)
        self._message_document_handler.register(handler)

    def register_animation_handler(self, handler: HandleFunction):
        if MESSAGE_ANIMATION not in self._update_types:
            self._update_types.append(MESSAGE_ANIMATION)
        self._message_animation_handler.register(handler)

    def register_audio_handler(self, handler: HandleFunction):
        if MESSAGE_AUDIO not in self._update_types:
            self._update_types.append(MESSAGE_AUDIO)
        self._message_audio_handler.register(handler)

    def register_contact_handler(self, handler: HandleFunction):
        if MESSAGE_CONTACT not in self._update_types:
            self._update_types.append(MESSAGE_CONTACT)
        self._message_contact_handler.register(handler)

    def register_game_handler(self, handler: HandleFunction):
        if MESSAGE_GAME not in self._update_types:
            self._update_types.append(MESSAGE_GAME)
        self._message_game_handler.register(handler)

    def register_invoice_handler(self, handler: HandleFunction):
        if MESSAGE_INVOICE not in self._update_types:
            self._update_types.append(MESSAGE_INVOICE)
        self._message_invoice_handler.register(handler)

    def register_left_chat_member_handler(self, handler: HandleFunction):
        if MESSAGE_LEFT_CHAT_MEMBER not in self._update_types:
            self._update_types.append(MESSAGE_LEFT_CHAT_MEMBER)
        self._message_left_chat_member_handler.register(handler)

    def register_location_handler(self, handler: HandleFunction):
        if MESSAGE_LOCATION not in self._update_types:
            self._update_types.append(MESSAGE_LOCATION)
        self._message_location_handler.register(handler)

    def register_new_chat_members_handler(self, handler: HandleFunction):
        if MESSAGE_NEW_CHAT_MEMBERS not in self._update_types:
            self._update_types.append(MESSAGE_NEW_CHAT_MEMBERS)
        self._message_new_chat_members_handler.register(handler)

    def register_new_chat_photo_handler(self, handler: HandleFunction):
        if MESSAGE_NEW_CHAT_PHOTO not in self._update_types:
            self._update_types.append(MESSAGE_NEW_CHAT_PHOTO)
        self._message_new_chat_photo_handler.register(handler)

    def register_new_chat_title_handler(self, handler):
        if MESSAGE_NEW_CHAT_TITLE not in self._update_types:
            self._update_types.append(MESSAGE_NEW_CHAT_TITLE)
        self._message_new_chat_title_handler.register(handler)

    def register_photo_handler(self, handler: HandleFunction):
        if MESSAGE_PHOTO not in self._update_types:
            self._update_types.append(MESSAGE_PHOTO)
        self._message_photo_handler.register(handler)

    def register_sticker_handler(self, handler: HandleFunction):
        if MESSAGE_STICKER not in self._update_types:
            self._update_types.append(MESSAGE_STICKER)
        self._message_sticker_handler.register(handler)

    def register_successful_payment_handler(self, handler: HandleFunction):
        if MESSAGE_SUCCESSFUL_PAYMENT not in self._update_types:
            self._update_types.append(MESSAGE_SUCCESSFUL_PAYMENT)
        self._message_successful_payment_handler.register(handler)

    def register_venue_handler(self, handler: HandleFunction):
        if MESSAGE_VENUE not in self._update_types:
            self._update_types.append(MESSAGE_VENUE)
        self._message_venue_handler.register(handler)

    def register_video_handler(self, handler: HandleFunction):
        if MESSAGE_VIDEO not in self._update_types:
            self._update_types.append(MESSAGE_VIDEO)
        self._message_video_handler.register(handler)

    def register_video_note_handler(self, handler: HandleFunction):
        if MESSAGE_VIDEO_NOTE not in self._update_types:
            self._update_types.append(MESSAGE_VIDEO_NOTE)
        self._message_video_note_handler.register(handler)

    def register_voice_handler(self, handler: HandleFunction):
        if MESSAGE_VOICE not in self._update_types:
            self._update_types.append(MESSAGE_VOICE)
        self._message_voice_handler.register(handler)

    async def _run_statements(self, context: BaseContext):
        for update_type in self._update_types:
            statement_key = f'is_{update_type}'
            handler_key = f'_{update_type}_handler'

            if getattr(context, statement_key):
                handler = getattr(self, handler_key)
                context.update_type = update_type
                await handler.handle(context)

    async def _run_middlewares(self, context: BaseContext) -> bool:
        for middleware in self._middlewares:
            if await middleware(context):
                return True

        return False

    async def handle(self, update: dict):
        await self.handle_context(BaseContext(Update.from_dict(update)))

    async def handle_context(self, context: BaseContext):
        if await self._run_middlewares(context):
            return

        await self._run_statements(context)
