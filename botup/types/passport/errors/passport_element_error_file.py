from .base_element_error import BaseElementError


class PassportElementErrorFile(BaseElementError):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_hash = kwargs.get('file_hash')
