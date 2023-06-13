from .base import StringConstant


class InputFileType(StringConstant):
    pass


STORED = InputFileType('stored')
URL = InputFileType('url')
PATH = InputFileType('path')
