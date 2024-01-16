import logging

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram import types

class CustomMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 6):
        BaseMiddleware.__init__(self)
        self.limit = limit

    async def on_pre_process_update(self, message: types.Message, data: dict):
        logging.info("Новый апдейт")
        logging.info("Pre-process Update")
        logging.info("Next: Process Update")
        print("On process message", message.text)
