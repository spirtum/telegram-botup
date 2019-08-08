class BaseObject:
    NESTED_KEYS = list()

    def as_dict(self):
        result = {key: value for key, value in vars(self).items() if value is not None}
        for key in self.NESTED_KEYS:
            if key in result:
                result[key] = result[key].as_dict()
        return result
