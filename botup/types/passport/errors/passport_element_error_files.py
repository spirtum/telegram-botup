from .base_element_error import BaseElementError


class PassportElementErrorFiles(BaseElementError):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_hashes = kwargs.get('file_hashes')
