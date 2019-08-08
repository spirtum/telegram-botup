from .animation import Animation
from .audio import Audio
from .contact import Contact
from .document import Document
from .inline_keyboard_markup import InlineKeyboardMarkup
from .location import Location
from .message_entity import MessageEntity
from .photo_size import PhotoSize
from .poll import Poll
from .user import User
from .venue import Venue
from .video import Video
from .video_note import VideoNote
from .voice import Voice
from ..games.game import Game
from ..passport.passport_data import PassportData
from ..payments.invoice import Invoice
from ..payments.successfull_payment import SuccessfulPayment
from ..stickers.sticker import Sticker


class PinnedMessage:

    def __init__(self, **kwargs):
        self.message_id = kwargs.get('message_id')
        self.from_ = User(**kwargs['from']) if 'from' in kwargs else None
        self.date = kwargs.get('date')
        self.forward_from = User(**kwargs['forward_from']) if 'forward_from' in kwargs else None
        self.forward_signature = kwargs.get('forward_signature')
        self.forward_sender_name = kwargs.get('forward_sender_name')
        self.forward_date = kwargs.get('forward_date')
        self.reply_to_message = PinnedMessage(**kwargs['reply_to_message']) if 'reply_to_message' in kwargs else None
        self.edit_date = kwargs.get('edit_date')
        self.media_group_id = kwargs.get('media_group_id')
        self.author_signature = kwargs.get('author_signature')
        self.text = kwargs.get('text')
        self.entities = [MessageEntity(**v) for v in kwargs['entities']] if 'entities' in kwargs else []
        self.caption_entities = [MessageEntity(**v) for v in
                                 kwargs['caption_entities']] if 'caption_entities' in kwargs else []
        self.audio = Audio(**kwargs['audio']) if 'audio' in kwargs else None
        self.document = Document(**kwargs['document']) if 'document' in kwargs else None
        self.animation = Animation(**kwargs['animation']) if 'animation' in kwargs else None
        self.game = Game(**kwargs['game']) if 'game' in kwargs else None
        self.photo = [PhotoSize(**v) for v in kwargs['photo']] if 'photo' in kwargs else []
        self.sticker = Sticker(**kwargs['sticker']) if 'sticker' in kwargs else None
        self.video = Video(**kwargs['video']) if 'video' in kwargs else None
        self.voice = Voice(**kwargs['voice']) if 'voice' in kwargs else None
        self.video_note = VideoNote(**kwargs['video_note']) if 'video_note' in kwargs else None
        self.caption = kwargs.get('caption')
        self.contact = Contact(**kwargs['contact']) if 'contact' in kwargs else None
        self.location = Location(**kwargs['location']) if 'location' in kwargs else None
        self.venue = Venue(**kwargs['venue']) if 'venue' in kwargs else None
        self.poll = Poll(**kwargs['poll']) if 'poll' in kwargs else None
        self.new_chat_members = [User(**v) for v in kwargs['new_chat_members']] if 'new_chat_members' in kwargs else []
        self.left_chat_member = User(**kwargs['left_chat_member']) if 'left_chat_member' in kwargs else None
        self.new_chat_title = kwargs.get('new_chat_title')
        self.new_chat_photo = [PhotoSize(**v) for v in kwargs['new_chat_photo']] if 'new_chat_photo' in kwargs else []
        self.delete_chat_photo = kwargs.get('delete_chat_photo')
        self.group_chat_created = kwargs.get('group_chat_created')
        self.supergroup_chat_created = kwargs.get('supergroup_chat_created')
        self.channel_chat_created = kwargs.get('channel_chat_created')
        self.migrate_to_chat_id = kwargs.get('migrate_to_chat_id')
        self.migrate_from_chat_id = kwargs.get('migrate_from_chat_id')
        self.pinned_message = PinnedMessage(**kwargs['pinned_message']) if 'pinned_message' in kwargs else None
        self.invoice = Invoice(**kwargs['invoice']) if 'invoice' in kwargs else None
        self.successful_payment = SuccessfulPayment(
            **kwargs['successful_payment']) if 'successful_payment' in kwargs else None
        self.connected_website = kwargs.get('connected_website')
        self.passport_data = PassportData(**kwargs['passport_data']) if 'passport_data' in kwargs else None
        self.reply_markup = InlineKeyboardMarkup(**kwargs['reply_markup']) if 'reply_markup' in kwargs else None
