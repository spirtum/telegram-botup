from .poll_option import PollOption


class Poll:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.question = kwargs.get('question')
        self.options = [PollOption(**v) for v in kwargs['options']] if 'options' in kwargs else []
        self.is_closed = kwargs.get('is_closed')
