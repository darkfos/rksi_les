import json

from aiogram import Router, types, F
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext

from bot.filters import TeacherData, GroupsData
from bot.text import get_all_teachers, get_all_groups
from rksi_parse import parse_teachers, load_prepods_in_file, load_groups_in_file, all_groups, parse_lessons_for_student, \
    parse_lessons_for_teachers, load_prepods_to_csv, load_groups_to_csv
from bot.states import SampleData, GroupState
from utils import Database


callback_router = Router()


@callback_router.callback_query(TeacherData())
async def sel_prepods_button(callback_bt: types.CallbackQuery):
    all_teachers: list = await parse_teachers()

    if callback_bt.data == "list_btn":

        await callback_bt.message.reply(await get_all_teachers(all_teachers))

    elif callback_bt.data == "file_btn":
        #Запись данных в файл, необходимо для отправки
        await load_prepods_in_file(all_teachers)

        file_to_send: FSInputFile = FSInputFile("data/all_teachers.txt")
        await callback_bt.message.answer_document(document=file_to_send)

    else:
        await load_prepods_to_csv(all_teachers)

        file_csv = FSInputFile("data/all_teachers.csv")
        await callback_bt.message.answer_document(document=file_csv)


@callback_router.callback_query(GroupsData())
async def sel_groups_button(callback_bt: types.CallbackQuery):

    all_grp: list = await all_groups()
    text_all_grp: str = await get_all_groups(all_grp)

    if callback_bt.data == "list_gbtn":

        await callback_bt.message.reply(text=text_all_grp)

    elif callback_bt.data == "file_gbtn":

        await load_groups_in_file(all_grp)

        file_to_send: FSInputFile = FSInputFile("data/all_groups.txt")
        await callback_bt.message.answer_document(document=file_to_send)

    else:

        await load_groups_to_csv(all_grp)

        file_csv = FSInputFile("data/add_groups.csv")
        await callback_bt.message.answer_document(document=file_csv)



@callback_router.callback_query(F.data.endswith("stbtn"))
async def button_to_start_menu(callback_st_mn: types.CallbackQuery, state: FSMContext):
    if callback_st_mn.data == "shablon_stbtn":
        md = Database()
        res = await md.get_one_user(data={"tg_id": callback_st_mn.from_user.id})

        if res:
            await callback_st_mn.message.answer("Вы были найдены в базе данных, ожидайте ответа")
            result_all_message: str = await show_all_lessons(name_group=res["name_group"])
            await callback_st_mn.message.answer(result_all_message, parse_mode="HTML")

        else:
            await callback_st_mn.message.reply("Введите ваше имя")
            await state.set_state(SampleData.name)
    else:
        await callback_st_mn.message.answer("Вы выбрали ручной поиск, введите <b>группу</b>", parse_mode="HTML")
        await state.set_state(GroupState.name_group)


async def show_all_lessons(name_group: str = None, name_teacher: str = None) -> str:

    if name_group:
        to_find = "lessons_schedule.json"
        text_find = "Расписание пар для группы <b>{0}</b>".format(name_group)
        get_lessons = await parse_lessons_for_student(name_group)

    else:
        to_find = "lessons_schedule_for_teachers.json"
        text_find = "Расписание пар для Преподавателя <b>{0}</b>".format(name_teacher)
        get_lessons = await parse_lessons_for_teachers(name_teacher)

    with open(f"data/{to_find}", "r") as js_file:
        file = json.load(js_file)

        days: list = ["январ", "феврал", "март", "апрел", "мая", "июн", "июл", "август", "сентябр", "октябр", "ноябр",
                      "декабр"]
        all_prepods = await parse_teachers()
        message: str = text_find
        count_to_res: int = 0

        for day in file.keys():
            for info_less in file[day]:
                if any([day in info_less for day in days]):
                    message += "\n\n" + "📅 " + f"<b>{info_less}</b>" + "\n\n"
                elif any([teacher in info_less for teacher in all_prepods]):
                    message += "👨‍🎓 " + info_less + "\n\n"
                elif info_less[0].isdigit() and info_less[1].isdigit() and name_teacher != None and count_to_res >= 3:
                    message += "\n\n" + "⏳ " + info_less
                elif info_less[0].isdigit() and info_less[1].isdigit():
                    message += "⏳ " + info_less + "\n"
                else:
                    if name_teacher:
                        message += "\n" + "📚 " + info_less
                    else:
                        message += "📚 " + info_less + "\n"

                count_to_res += 1

        return message