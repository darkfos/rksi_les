import datetime


from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext


from bot.text import help_text, start_text
from bot.handlers import find_teacher_lessons, show_all_lessons
from bot.states import TeacherState, GroupState, ChoicePeople
from bot.keyboards import sel_to_teachers, get_start_bt, sel_to_groups


from rksi_parse import parse_teachers, all_groups as al_grp

# Роутер для обработки комманд
command_router = Router()


# Обработчик команды "start"
@command_router.message(CommandStart())
async def start_command(message: Message):
    await message.answer_video(video=FSInputFile("static/img/cat_boss.gif", "cats"))
    await message.reply(text=start_text, reply_markup=await get_start_bt(), parse_mode="HTML")


# ------------------------------------------- #


# Обработчик команды "help"
@command_router.message(Command("help"))
async def help_command(message: Message):
    photo_to_send: FSInputFile = FSInputFile("static/img/rksi.jpg")
    await message.answer_photo(photo=photo_to_send, caption=help_text, parse_mode="HTML")


# ------------------------------------------- #


# Обработчик команды "prepods"
@command_router.message(Command("prepods"))
async def all_teachers(message: Message):
    await message.answer("⚖️ <b>Выберите</b> пункт для получения формата ответа: ", parse_mode="HTML", reply_markup=await sel_to_teachers())


# ------------------------------------------- #


# Обработчик команды "groups"
@command_router.message(Command("groups"))
async def all_groups(message: Message):
    await message.answer("⚖️ <b>Выберите</b> пункт для получения формата ответа: ", parse_mode="HTML", reply_markup=await sel_to_groups())


# ------------------------------------------- #


# Обработчик команды "prepod_name"
@command_router.message(Command("prepod_name"))
async def get_info_by_teacher(message: Message, state: FSMContext):
    await state.set_state(TeacherState.name)
    await message.answer("✍🏼 Введите фамилию или полные инициалы преподавателя")


# ------------------------------------------- #


# Обработчик команды "lessons_group"
@command_router.message(Command("lessons_group"))
async def get_lessons_for_group(message: Message, state: FSMContext):
    await state.set_state(GroupState.name_group)
    await message.answer("✍🏼 Введите название <b>группы</b>", parse_mode="HTML")


# ------------------------------------------- #


# Обработчик команды "lessons_now"
@command_router.message(Command("lessons_now"))
async def get_lessons_now(message: Message, state: FSMContext):
    await message.answer("✍🏼 Введите вашу роль - (студент, преподаватель)")
    await state.set_state(ChoicePeople.choice_pers)

# ------------------------------------------- #


# Обработчик состояния - Получение инициалов преподавателя
@command_router.message(TeacherState.name)
async def get_name_teacher(message: Message, state: FSMContext):
    all_teachers: list = await parse_teachers()
    answer_teacher: bool = any([message.text.lower() in teacher.lower() for teacher in all_teachers])

    if answer_teacher:
        await state.update_data(name=message.text)
        await state.clear()
        lessons_for_teacher: str = await find_teacher_lessons(message)
        await message.answer(text=lessons_for_teacher, parse_mode="HTML")

    else:

        await message.answer("❌ Преподаватель не был найден")


# ------------------------------------------- #


# Обработчик состояния - Получение типа юзера
@command_router.message(ChoicePeople.choice_pers)
async def get_pers_info(message: Message, state: FSMContext):
    if message.text.lower() in ("студент", "преподаватель"):
        await state.update_data(choice_pres=message.text.lower())
        await state.set_state(ChoicePeople.name_pers)

        if message.text.lower() == "студент":
            await message.answer("✍🏼 Введите учебную группу")
        else:
            await message.answer("✍🏼 Введите инициалы преподавателя")
    else:
        await message.answer("❌ Неверные данные")


# ------------------------------------------- #


# Обработчик состояния - Получение названия типа юзера
@command_router.message(ChoicePeople.name_pers)
async def get_pers_info_name(message: Message, state: FSMContext):

    pers_info = await state.get_data()
    today_data = datetime.date.today()
    day_week = today_data.weekday()

    monts: dict = {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря"
    }

    month_today: str = monts.get(today_data.month)
    day_today: int = today_data.day

    if pers_info["choice_pres"] == "студент":
        all_groups_for_1d: bool = any([message.text.upper() == group for group in await al_grp()])
        if all_groups_for_1d:
            await state.update_data(name_pers=message.text.upper())
            await state.clear()

            message_for_1d = await show_all_lessons(name_group=message.text.upper())

            lessons_for_student_1d: str = ""

            if day_week not in (6, 5):
                for line in message_for_1d.split("\n"):
                    if f"{day_today+1} {month_today}" in line:
                        break
                    else:
                        lessons_for_student_1d += line + "\n"

            if lessons_for_student_1d and len(lessons_for_student_1d.split("\n")) > 3:

                await message.answer(text=lessons_for_student_1d, parse_mode="HTML")

            else:

                await message.answer(text="На сегодня пар нет")

        else:

            await message.answer("❌ Неверные данные")

    elif pers_info["choice_pres"] == "преподаватель":

        name_teacher_for_1d: str = ""

        for teacher in await parse_teachers():
            if message.text.lower() in teacher.lower():
                name_teacher_for_1d = teacher
                break

        if name_teacher_for_1d:
            await state.update_data(name_pers=message.text.upper())
            await state.clear()

            message_for_1d = await show_all_lessons(name_teacher=name_teacher_for_1d)


            lessons_for_teachers_1d: str = ""

            if day_week not in (6, 5):
                for line in message_for_1d.split("\n"):
                    if f"{day_today+1} {month_today}" in line:
                        break
                    else:
                        lessons_for_teachers_1d += line + "\n"

            if lessons_for_teachers_1d and (len(lessons_for_teachers_1d.split("\n")) > 3):

                print(lessons_for_teachers_1d.split("\n"))

                await message.answer(text=lessons_for_teachers_1d, parse_mode="HTML")

            else:

                await message.answer(text="На сегодня пар нет")

        else:

            await message.answer("❌ Неверные данные")