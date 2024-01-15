import config

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command
from .text import help_text
from rksi_parse import parse_teachers
from aiogram.fsm.context import FSMContext
from .states import TeacherState

main_router = Router()

@main_router.message(CommandStart())
async def start_command(message: Message):
    await message.reply("Привет {0}!".format(message.from_user.full_name))


@main_router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(text=help_text, parse_mode="HTML")


@main_router.message(Command("prepods"))
async def all_teachers(message: Message):
    all_teachers: list = await parse_teachers()
    answer: str = ""
    for teacher in all_teachers:
        answer += teacher + "\n"

    await message.answer("<u>Список всех преподавателей: </u>\n{0}".format(answer), parse_mode="HTML")


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
        await message.answer("Такого нет...")

async def start_bot():
    rksi_bot = Bot(token=config.API_KEY_TG)
    storage = MemoryStorage()
    dp = Dispatcher(bot=rksi_bot, storage=storage)
    dp.include_router(
        main_router
    )

    await dp.start_polling(rksi_bot)