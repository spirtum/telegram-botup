class PollOption:

    def __init__(self, **kwargs):
        self.text = kwargs.get('text')
        self.voter_count = kwargs.get('voter_count')
