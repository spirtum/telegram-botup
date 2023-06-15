from .base import StringConstant


class PassportElementErrorSource(StringConstant):
    pass


DATA = PassportElementErrorSource('data')
FRONT_SIDE = PassportElementErrorSource('front_side')
REVERSE_SIDE = PassportElementErrorSource('reverse_side')
SELFIE = PassportElementErrorSource('selfie')
FILE = PassportElementErrorSource('file')
FILES = PassportElementErrorSource('files')
TRANSLATION_FILE = PassportElementErrorSource('translation_file')
TRANSLATION_FILES = PassportElementErrorSource('translation_files')
UNSPECIFIED = PassportElementErrorSource('unspecified')
