from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from rksi_parse import all_groups
from bot.filters import FindTeacherName, FilterChoice
from bot.keyboards import get_student_choice_bt
from bot.states import TeacherState, SampleData
from utils import Database

msg_router = Router()

@msg_router.message(FindTeacherName())
async def new_msg(message: types.Message):
    await message.answer("Преподаватель был найден в БД")


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
        await message.answer("Такой группы не существует. Повторите попытку!")


@msg_router.message()
async def processing_other_messages(message: types.Message):
    await message.answer("Не могу распознать ваш текст.\nОжидается команда или инициалы преподавателя")