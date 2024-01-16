import logging
import cachetools

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram import types

from typing import Callable, Dict, Any, Awaitable

class CustomMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 2):
        BaseMiddleware.__init__(self)
        self.limit = cachetools.TTLCache(maxsize=1000, ttl=limit)


    async def __call__(self,
                       handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
                       event: types.Message,
                       data: Dict[str, Any]) -> Any:
        if event.chat.id in self.limit:
            return
        else:
            self.limit[event.chat.id] = None
        return await handler(event, data)