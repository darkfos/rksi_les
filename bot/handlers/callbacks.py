from aiogram import Router, types, F
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext

from bot.filters import TeacherData, GroupsData
from bot.text import get_all_teachers, get_all_groups
from rksi_parse import parse_teachers, load_prepods_in_file, load_groups_in_file, all_groups
from bot.states import SampleData
from utils import Database


callback_router = Router()


@callback_router.callback_query(TeacherData())
async def sel_prepods_button(callback_bt: types.CallbackQuery):
    all_teachers: list = await parse_teachers()

    if callback_bt.data == "list_btn":

        await callback_bt.message.reply(await get_all_teachers(all_teachers))

    else:
        #Запись данных в файл, необходимо для отправки
        await load_prepods_in_file(all_teachers)

        file_to_send: FSInputFile = FSInputFile("data/all_teachers.txt")
        await callback_bt.message.answer_document(document=file_to_send)

    await callback_bt.answer("Вы выбрали кнопку {0}".format(callback_bt.data))


@callback_router.callback_query(GroupsData())
async def sel_groups_button(callback_bt: types.CallbackQuery):

    all_grp: list = await all_groups()
    text_all_grp: str = await get_all_groups(all_grp)

    if callback_bt.data == "list_gbtn":

        await callback_bt.message.reply(text=text_all_grp)

    else:

        await load_groups_in_file(all_grp)

        file_to_send: FSInputFile = FSInputFile("data/all_groups.txt")
        await callback_bt.message.answer_document(document=file_to_send)


@callback_router.callback_query(F.data.endswith("stbtn"))
async def button_to_start_menu(callback_st_mn: types.CallbackQuery, state: FSMContext):
    if callback_st_mn.data == "shablon_stbtn":
        md = Database().get_one_user(
            data={"tg_id": callback_st_mn.message.message_id}
        )

        if md:
            await callback_st_mn.message.answer("Вы были найдены в базе данных, ожидайте ответа")

        else:
            await callback_st_mn.message.reply("Введите ваше имя")
            await state.set_state(SampleData.name)
    else:
        await callback_st_mn.message.answer("Вы выбрали ручной поиск, введите группу")
