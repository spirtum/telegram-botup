from .base import StringConstant


class ChatMemberStatus(StringConstant):
    pass


CREATOR = ChatMemberStatus('creator')
ADMINISTRATOR = ChatMemberStatus('administrator')
MEMBER = ChatMemberStatus('member')
RESTRICTED = ChatMemberStatus('restricted')
LEFT = ChatMemberStatus('left')
KICKED = ChatMemberStatus('kicked')
