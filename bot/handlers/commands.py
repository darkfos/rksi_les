import config

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext


from bot.text import help_text, get_all_groups
from rksi_parse import parse_teachers, all_groups
from bot.states import TeacherState
from bot.keyboards import sel_to_teachers, get_start_bt, sel_to_groups

command_router = Router()

@command_router.message(CommandStart())
async def start_command(message: Message):
    await message.reply("Привет {0}! Выбери пункт меню".format(message.from_user.full_name), reply_markup=await get_start_bt(),)


@command_router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(text=help_text, parse_mode="HTML")


@command_router.message(Command("prepods"))
async def all_teachers(message: Message):
    await message.answer("<b>Выберите</b> пункт для получения формата ответа: ", parse_mode="HTML", reply_markup=await sel_to_teachers())


@command_router.message(Command("groups"))
async def all_groups(message: Message):
    await message.answer("<b>Выберите</b> пункт для получения формата ответа: ", parse_mode="HTML", reply_markup=await sel_to_groups())


@command_router.message(Command("prepod_name"))
async def get_info_by_teacher(message: Message, state: FSMContext):
    await state.set_state(TeacherState.name)
    await message.answer("Пожалуйста введите фамилию или полные инициалы преподавателя..")

@command_router.message(TeacherState.name)
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