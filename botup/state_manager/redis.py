from typing import Optional

from redis.asyncio import Redis

from botup.state_manager.base import Singleton, StateManager


class RedisStateManager(StateManager, metaclass=Singleton):

    def __init__(self, url: str):
        super().__init__()
        self.redis = Redis.from_url(url, decode_responses=True)

    async def get_path(self, chat_id: int) -> Optional[str]:
        return await self.get(chat_id, 'path', 'botup')

    async def set_path(self, chat_id: int, path: str):
        await self.set(chat_id, 'path', path, 'botup')

    async def get(self, chat_id: int, key: str, section: str = 'botup-user') -> Optional[str]:
        return await self.redis.get(f'{section}:{chat_id}:{key}')

    async def set(self, chat_id: int, key: str, value: str, section: str = 'botup-user'):
        await self.redis.set(f'{section}:{chat_id}:{key}', value)

    async def delete(self, chat_id: int, key: str, section: str = 'botup-user'):
        await self.redis.delete(f'{section}:{chat_id}:{key}')
