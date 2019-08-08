class Contact:

    def __init__(self, **kwargs):
        self.phone_number = kwargs.get('phone_number')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.user_id = kwargs.get('user_id')
        self.vcard = kwargs.get('vcard')
