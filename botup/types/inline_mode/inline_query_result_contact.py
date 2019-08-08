from .inline_query_result import InlineQueryResult


class InlineQueryResultContact(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'contact'
        self.phone_number = kwargs.get('phone_number')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.vcard = kwargs.get('vcard')
        self.thumb_url = kwargs.get('thumb_url')
        self.thumb_width = kwargs.get('thumb_width')
        self.thumb_height = kwargs.get('thumb_height')
