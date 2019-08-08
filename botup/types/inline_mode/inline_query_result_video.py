from .inline_query_result import InlineQueryResult


class InlineQueryResultVideo(InlineQueryResult):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'video'
        self.video_url = kwargs.get('video_url')
        self.mime_type = kwargs.get('mime_type')
        self.thumb_url = kwargs.get('thumb_url')
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
        self.video_width = kwargs.get('video_width')
        self.video_height = kwargs.get('video_height')
        self.video_duration = kwargs.get('video_duration')
        self.description = kwargs.get('description')
