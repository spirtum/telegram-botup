from typing import Optional

import aioredis

from .base import Singleton, StateManager


class RedisStateManager(StateManager, metaclass=Singleton):

    def __init__(self, url: str):
        super().__init__()
        self.redis = aioredis.from_url(url, decode_responses=True)

    async def get_path(self, chat_id: int) -> Optional[str]:
        return await self.redis.get(f'botup:{chat_id}:path')

    async def set_path(self, chat_id: int, path: str):
        await self.redis.set(f'botup:{chat_id}:path', path)

    async def get(self, chat_id: int, key: str) -> Optional[str]:
        return await self.redis.get(f'botup-user:{chat_id}:{key}')

    async def set(self, chat_id: int, key: str, value: str):
        await self.redis.set(f'botup-user:{chat_id}:{key}', value)
