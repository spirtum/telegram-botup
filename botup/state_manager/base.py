from typing import Optional, Dict


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class StateManager:

    async def get(self, chat_id: int) -> Optional[str]:
        raise NotImplementedError()

    async def set(self, chat_id: int, path: str):
        raise NotImplementedError()


class DictStateManager(StateManager, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self._data: Dict[str, str] = {}

    async def get(self, chat_id: int) -> Optional[str]:
        return self._data.get(str(chat_id))

    async def set(self, chat_id: int, path: str):
        self._data[str(chat_id)] = path
