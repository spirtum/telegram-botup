from .input_contact_message_content import InputContactMessageContent
from .input_location_message_content import InputLocationMessageContent
from .input_text_message_content import InputTextMessageContent
from .input_venue_message_content import InputVenueMessageContent
from ..common.inline_keyboard_markup import InlineKeyboardMarkup


class InlineQueryResult:

    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.id = kwargs.get('id')
        self.reply_markup = InlineKeyboardMarkup(**kwargs['reply_markup']) if 'reply_markup' in kwargs else None
        self.input_message_content = None
        imc = kwargs.get('input_message_content')
        if imc:
            if 'phone_number' in imc:
                self.input_message_content = InputContactMessageContent(**imc)
            elif 'latitude' in imc and 'address' in imc:
                self.input_message_content = InputVenueMessageContent(**imc)
            elif 'latitude' in imc:
                self.input_message_content = InputLocationMessageContent(**imc)
            elif 'message_text' in imc:
                self.input_message_content = InputTextMessageContent(**imc)

    def as_dict(self):
        result = {k: v for k, v in vars(self).items() if v}
        result['reply_markup'] = self.reply_markup.as_dict() if self.reply_markup else dict()
        result['input_message_content'] = self.input_message_content.as_dict() if self.input_message_content else dict()
        return result
