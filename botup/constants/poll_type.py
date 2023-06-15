from .base import StringConstant


class PollType(StringConstant):
    pass


REGULAR = PollType('regular')
QUIZ = PollType('quiz')
