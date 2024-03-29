import config

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from bot.middleware import CustomMiddleware
from bot.handlers import *
from bot.utils_bot import set_all_commands


# Метод запуск бота
async def start_bot():
    rksi_bot = Bot(token=config.API_KEY_TG)
    storage = MemoryStorage()
    dp = Dispatcher(bot=rksi_bot, storage=storage)
    dp.message.middleware(CustomMiddleware())

    # Подключение всех Router's
    dp.include_routers(
        command_router,
        callback_router,
        msg_router,
    )

    # Установка description
    await set_all_commands(rksi_bot)

    # Запуск бота
    await dp.start_polling(rksi_bot)