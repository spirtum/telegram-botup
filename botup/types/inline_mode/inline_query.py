from ..common.location import Location
from ..common.user import User


class InlineQuery:
    __slots__ = ['id', 'from_', 'location', 'query', 'offset']

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.from_ = User(**kwargs.get('from'))
        self.location = Location(**kwargs['location']) if 'location' in kwargs else None
        self.query = kwargs.get('query')
        self.offset = kwargs.get('offset')
