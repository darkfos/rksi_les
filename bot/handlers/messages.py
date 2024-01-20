from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from rksi_parse import all_groups, parse_lessons_for_teachers, parse_teachers
from bot.filters import FindTeacherName, FilterChoice
from bot.keyboards import get_student_choice_bt
from bot.states import TeacherState, SampleData, GroupState
from bot.handlers import show_all_lessons
from utils import Database

msg_router = Router()

@msg_router.message(FindTeacherName())
async def new_msg(message: types.Message):
    answer_to_teacher: str = await find_teacher_lessons(message)
    await message.answer(text=answer_to_teacher, parse_mode="HTML")


@msg_router.message(FilterChoice())
async def teach_or_student(message: types.Message, state: FSMContext):
    if message.text.lower() == "студент":
        await message.answer("Пункт меню 'Студент', выберите нужный вам пункт", reply_markup=await get_student_choice_bt())
    else:
        await state.set_state(TeacherState.name)
        await message.answer("Жду фамилию преподавателя")

@msg_router.message(SampleData.name)
async def get_name_user(message: types.Message, state: FSMContext):
    await message.answer("Отлично, теперь введи свою группу")
    await state.update_data(name=message.text)
    await state.set_state(SampleData.name_group)

@msg_router.message(SampleData.name_group)
async def get_name_grp_user(message: types.Message, state: FSMContext):
    all_group: list = await all_groups()

    if message.text in all_group:
        await message.answer("Отлично, ваш шаблон был создан.")
        await state.update_data(name_group=message.text)
        all_info = await state.get_data()
        await state.clear()

        all_info["tg_id"] = message.from_user.id
        await Database().add_one_user(data=all_info)

    else:
        await message.answer("Такой <b>группы</b> не существует. Повторите попытку!", parse_mode="HTML")


@msg_router.message(GroupState.name_group)
async def name_group_result(clb_answer: types.Message, state: FSMContext):
    all_group: list = await all_groups()
    if clb_answer.text in all_group:
        await state.update_data(name_group=clb_answer.text)
        await state.clear()
        await clb_answer.answer(await show_all_lessons(clb_answer.text), parse_mode="HTML")
    else:
        await clb_answer.answer("<b>Группа</b> не была найдена, попробуйте ещё раз.", parse_mode="HTML")


@msg_router.message()
async def processing_other_messages(message: types.Message):
    if message.text in await all_groups():
        await message.answer(await show_all_lessons(message.text), parse_mode="HTML")
    else:
        await message.answer("Не могу распознать ваш текст.\nОжидается команда или инициалы преподавателя")

async def find_teacher_lessons(message: types.Message) -> str:
    all_teachers: list = await parse_teachers()
    name_teacher: str = ""

    for teacher in all_teachers:
        if message.text in teacher:
            name_teacher = teacher
            break

    await parse_lessons_for_teachers(name_teacher)
    await message.answer("⏳ Преподаватель был найден, ожидайте ответа...")

    result: str = await show_all_lessons(name_teacher=name_teacher)

    return result