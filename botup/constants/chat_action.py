from .base import StringConstant


class ChatAction(StringConstant):
    pass


TYPING = ChatAction('typing')
UPLOAD_PHOTO = ChatAction('upload_photo')
RECORD_VIDEO = ChatAction('record_video')
UPLOAD_VIDEO = ChatAction('upload_video')
RECORD_VOICE = ChatAction('record_voice')
UPLOAD_VOICE = ChatAction('upload_voice')
UPLOAD_DOCUMENT = ChatAction('upload_document')
CHOOSE_STICKER = ChatAction('choose_sticker')
FIND_LOCATION = ChatAction('find_location')
RECORD_VIDEO_NOTE = ChatAction('record_video_note')
UPLOAD_VIDEO_NOTE = ChatAction('upload_video_note')
