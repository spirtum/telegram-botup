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

    async def get(self, chat_id: int, key: str, section: str = 'botup-user') -> Optional[str]:
        raise NotImplementedError()

    async def set(self, chat_id: int, key: str, value: str, section: str = 'botup-user'):
        raise NotImplementedError()

    async def delete(self, chat_id: int, key: str, section: str = 'botup-user'):
        raise NotImplementedError()


class DictStateManager(StateManager, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self._data: Dict[str, Dict] = {}

    def _get_user_dict(self, chat_id: int, section: str) -> dict:
        section_dict = self._data.setdefault(section, {})
        return section_dict.setdefault(str(chat_id), {})

    async def get_path(self, chat_id: int) -> Optional[str]:
        user_dict = self._get_user_dict(chat_id, 'botup')
        return user_dict.get('path')

    async def set_path(self, chat_id: int, path: str):
        user_dict = self._get_user_dict(chat_id, 'botup')
        user_dict['path'] = path

    async def get(self, chat_id: int, key: str, section: str = 'botup-user') -> Optional[str]:
        user_dict = self._get_user_dict(chat_id, section)
        return user_dict.get(key)

    async def set(self, chat_id: int, key: str, value: str, section: str = 'botup-user'):
        user_dict = self._get_user_dict(chat_id, section)
        user_dict[key] = value

    async def delete(self, chat_id: int, key: str, section: str = 'botup-user'):
        user_dict = self._get_user_dict(chat_id, section)
        user_dict.pop(key, None)
