from .base import StringConstant


class BotCommandScopeType(StringConstant):
    pass


DEFAULT = BotCommandScopeType('default')
ALL_PRIVATE_CHATS = BotCommandScopeType('all_private_chats')
ALL_GROUP_CHATS = BotCommandScopeType('all_group_chats')
ALL_CHAT_ADMINISTRATORS = BotCommandScopeType('all_chat_administrators')
CHAT = BotCommandScopeType('chat')
CHAT_ADMINISTRATORS = BotCommandScopeType('chat_administrators')
CHAT_MEMBER = BotCommandScopeType('chat_member')
