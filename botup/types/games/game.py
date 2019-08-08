from ..common.animation import Animation
from ..common.message_entity import MessageEntity
from ..common.photo_size import PhotoSize


class Game:

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.photo = [PhotoSize(**v) for v in kwargs['photo']] if 'photo' in kwargs else []
        self.text = kwargs.get('text')
        self.text_entities = [MessageEntity(**v) for v in kwargs['text_entities']] if 'text_entities' in kwargs else []
        self.animation = Animation(**kwargs['animation']) if 'animation' in kwargs else None
