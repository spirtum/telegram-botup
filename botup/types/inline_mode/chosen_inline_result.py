from ..common.location import Location
from ..common.user import User


class ChosenInlineResult:

    def __init__(self, **kwargs):
        self.result_id = kwargs.get('result_id')
        self.from_ = User(**kwargs['from'])
        self.location = Location(**kwargs['location']) if 'location' in kwargs else None
        self.inline_message_id = kwargs.get('inline_message_id')
        self.query = kwargs.get('query')
