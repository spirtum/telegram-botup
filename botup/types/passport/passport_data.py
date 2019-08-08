from .encrypted_credentials import EncryptedCredentials
from .encrypted_passport_element import EncryptedPassportElement


class PassportData:

    def __init__(self, **kwargs):
        self.data = [EncryptedPassportElement(**v) for v in kwargs['data']] if 'data' in kwargs else []
        self.credentials = EncryptedCredentials(**kwargs['credentials']) if 'credentials' in kwargs else None
