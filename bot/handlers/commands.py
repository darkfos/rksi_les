import config

from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext


from bot.text import help_text, start_text
from bot.handlers import find_teacher_lessons
from rksi_parse import parse_teachers
from bot.states import TeacherState, GroupState
from bot.keyboards import sel_to_teachers, get_start_bt, sel_to_groups

command_router = Router()

@command_router.message(CommandStart())
async def start_command(message: Message):
    await message.reply(text=start_text, reply_markup=await get_start_bt(), parse_mode="HTML")


@command_router.message(Command("help"))
async def help_command(message: Message):
    photo_to_send: FSInputFile = FSInputFile("static/img/rksi.jpg")
    await message.answer_photo(photo=photo_to_send, caption=help_text, parse_mode="HTML")


@command_router.message(Command("prepods"))
async def all_teachers(message: Message):
    await message.answer("⚖️ <b>Выберите</b> пункт для получения формата ответа: ", parse_mode="HTML", reply_markup=await sel_to_teachers())


@command_router.message(Command("groups"))
async def all_groups(message: Message):
    await message.answer("⚖️ <b>Выберите</b> пункт для получения формата ответа: ", parse_mode="HTML", reply_markup=await sel_to_groups())


@command_router.message(Command("prepod_name"))
async def get_info_by_teacher(message: Message, state: FSMContext):
    await state.set_state(TeacherState.name)
    await message.answer("✍🏼 Введите фамилию или полные инициалы преподавателя")


@command_router.message(Command("lessons_group"))
async def get_lessons_for_group(message: Message, state: FSMContext):
    await state.set_state(GroupState.name_group)
    await message.answer("✍🏼 Введите название <b>группы</b>", parse_mode="HTML")


@command_router.message(TeacherState.name)
async def get_name_teacher(message: Message, state: FSMContext):
    all_teachers: list = await parse_teachers()
    answer_teacher: list = any([message.text in teacher for teacher in all_teachers])
    if answer_teacher:
        await state.update_data(name=message.text)
        await state.clear()
        lessons_for_teacher: str = await find_teacher_lessons(message)
        await message.answer(text=lessons_for_teacher, parse_mode="HTML")
    else:
        await message.answer("❌ Преподаватель не был найден")