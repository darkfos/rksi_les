import config

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command

main_router = Router()

@main_router.message(CommandStart())
async def start_command(message: Message):
    await message.reply("Привет {0}!".format(message.from_user.full_name))


@main_router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Мой перечень команд...")



async def start_bot():
    rksi_bot = Bot(token=config.API_KEY_TG)
    storage = MemoryStorage()
    dp = Dispatcher(bot=rksi_bot, storage=storage)
    dp.include_router(
        main_router
    )

    await dp.start_polling(rksi_bot)