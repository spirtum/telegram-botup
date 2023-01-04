from typing import Optional, Dict


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class StateManager:

    async def get_path(self, chat_id: int) -> Optional[str]:
        raise NotImplementedError()

    async def set_path(self, chat_id: int, path: str):
        raise NotImplementedError()

    async def get(self, chat_id: int, key: str) -> Optional[str]:
        raise NotImplementedError()

    async def set(self, chat_id: int, key: str, value: str):
        raise NotImplementedError()


class DictStateManager(StateManager, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self._data: Dict[str, Dict] = {}

    def _get_user_dict(self, chat_id: int) -> dict:
        return self._data.setdefault(str(chat_id), {})

    async def get_path(self, chat_id: int) -> Optional[str]:
        user_dict = self._get_user_dict(chat_id)
        return user_dict.get('botup_path')

    async def set_path(self, chat_id: int, path: str):
        user_dict = self._get_user_dict(chat_id)
        user_dict['botup_path'] = path

    async def get(self, chat_id: int, key: str) -> Optional[str]:
        user_dict = self._get_user_dict(chat_id)
        return user_dict.get(key)

    async def set(self, chat_id: int, key: str, value: str):
        user_dict = self._get_user_dict(chat_id)
        user_dict[key] = value
