class InlineQueryResultGame:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'game'
        self.game_short_name = kwargs.get('game_short_name')
        del self.input_message_content
