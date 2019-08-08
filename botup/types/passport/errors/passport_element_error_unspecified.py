from .base_element_error import BaseElementError


class PassportElementErrorUnspecified(BaseElementError):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.element_hash = kwargs.get('element_hash')
