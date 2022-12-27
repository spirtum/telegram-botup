from .base import StringConstant


class MenuButtonType(StringConstant):
    pass


COMMANDS = MenuButtonType('commands')
WEB_APP = MenuButtonType('web_app')
DEFAULT = MenuButtonType('default')
