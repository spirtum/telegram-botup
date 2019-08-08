from ..common.user import User


class GameHighScore:

    def __init__(self, **kwargs):
        self.position = kwargs.get('position')
        self.user = User(**kwargs['user']) if 'user' in kwargs else None
        self.score = kwargs.get('score')
