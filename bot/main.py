import config

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext


from .text import help_text
from rksi_parse import parse_teachers
from .states import TeacherState
from .keyboards import sel_to_teachers
from .handlers import callback_router, msg_router
from .middleware import CustomMiddleware
from .utils_bot import set_all_commands

main_router = Router()

@main_router.message(CommandStart())
async def start_command(message: Message):
    await message.reply("Привет {0}!".format(message.from_user.full_name))


@main_router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(text=help_text, parse_mode="HTML")


@main_router.message(Command("prepods"))
async def all_teachers(message: Message):
    await message.answer("<b>Выберите</b> пункт для получения формата ответа: ", parse_mode="HTML", reply_markup=await sel_to_teachers())


@main_router.message(Command("prepod_name"))
async def get_info_by_teacher(message: Message, state: FSMContext):
    await state.set_state(TeacherState.name)
    await message.answer("Пожалуйста введите фамилию или полные инициалы преподавателя..")

@main_router.message(TeacherState.name)
async def get_name_teacher(message: Message, state: FSMContext):
    all_teachers: list = await parse_teachers()
    await state.update_data(name=message.text)
    flag_teacher = False
    for teacher in all_teachers:
        if message.text in teacher:
            await state.clear()
            await message.answer(text="Преподаватель был найден в БД")
            flag_teacher = True
    if not flag_teacher:
        await message.answer("Такого нет учителя нет, попробуйте ещё раз.")

async def start_bot():
    rksi_bot = Bot(token=config.API_KEY_TG)
    storage = MemoryStorage()
    dp = Dispatcher(bot=rksi_bot, storage=storage)
    dp.message.middleware(CustomMiddleware())
    dp.include_routers(
        main_router,
        callback_router,
        msg_router,
    )

    await set_all_commands(rksi_bot)
    await dp.start_polling(rksi_bot)