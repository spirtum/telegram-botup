from .base_element_error import BaseElementError


class PassportElementErrorDataField(BaseElementError):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.field_name = kwargs.get('field_name')
        self.data_hash = kwargs.get('data_hash')
