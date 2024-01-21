import logging
import cachetools

from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from typing import Callable, Dict, Any, Awaitable


class CustomMiddleware(BaseMiddleware):
    """
        Обработка количества запрос к боту, недопускает спам, limit = 1
    """
    def __init__(self, limit: int = 1):
        """
            Инициализация данных
            :param limit:
        """
        BaseMiddleware.__init__(self)
        self.limit = cachetools.TTLCache(maxsize=100000, ttl=limit)


    async def __call__(self,
                       handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
                       event: types.Message,
                       data: Dict[str, Any]) -> Any:
        """
            Магический метод для вызова класса
            :param handler:
            :param event:
            :param data:
            :return:
        """
        if event.chat.id in self.limit:
            return
        else:
            self.limit[event.chat.id] = None
        return await handler(event, data)