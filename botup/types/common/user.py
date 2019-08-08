class User:
    __slots__ = ['id', 'is_bot', 'first_name', 'last_name', 'username', 'language_code']

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.is_bot = kwargs.get('is_bot')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.username = kwargs.get('username')
        self.language_code = kwargs.get('language_code')
