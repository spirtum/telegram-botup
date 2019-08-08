from .passport_file import PassportFile


class EncryptedPassportElement:

    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.data = kwargs.get('data')
        self.phone_number = kwargs.get('phone_number')
        self.email = kwargs.get('email')
        self.files = [PassportFile(**v) for v in kwargs['files']] if 'files' in kwargs else []
        self.front_side = PassportFile(**kwargs['front_side']) if 'front_side' in kwargs else None
        self.reverse_side = PassportFile(**kwargs['reverse_side']) if 'reverse_side' in kwargs else None
        self.selfie = PassportFile(**kwargs['selfie']) if 'selfie' in kwargs else None
        self.translation = [PassportFile(**v) for v in kwargs['translation']] if 'translation' in kwargs else []
        self.hash = kwargs.get('hash')
