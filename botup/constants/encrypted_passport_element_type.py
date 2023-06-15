from .base import StringConstant


class EncryptedPassportElementType(StringConstant):
    pass


PERSONAL_DETAILS = EncryptedPassportElementType('personal_details')
PASSPORT = EncryptedPassportElementType('passport')
DRIVER_LICENSE = EncryptedPassportElementType('driver_license')
IDENTITY_CARD = EncryptedPassportElementType('identity_card')
INTERNAL_PASSPORT = EncryptedPassportElementType('internal_passport')
ADDRESS = EncryptedPassportElementType('address')
UTILITY_BILL = EncryptedPassportElementType('utility_bill')
BANK_STATEMENT = EncryptedPassportElementType('bank_statement')
RENTAL_AGREEMENT = EncryptedPassportElementType('rental_agreement')
PASSPORT_REGISTRATION = EncryptedPassportElementType('passport_registration')
TEMPORARY_REGISTRATION = EncryptedPassportElementType('temporary_registration')
PHONE_NUMBER = EncryptedPassportElementType('phone_number')
EMAIL = EncryptedPassportElementType('email')
