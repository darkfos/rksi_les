from aiogram import Router, types
from aiogram.types import FSInputFile

from bot.filters import TeacherData
from bot.text import get_all_teachers
from rksi_parse import parse_teachers, loat_prepods_in_file


callback_router = Router()


@callback_router.callback_query(TeacherData())
async def sel_prepods_button(callback_bt: types.CallbackQuery):
    all_teachers: list = await parse_teachers()

    if callback_bt.data == "list_btn":

        await callback_bt.message.reply(await get_all_teachers(all_teachers))

    else:
        #Запись данных в файл, необходимо для отправки
        await loat_prepods_in_file(all_teachers)

        file_to_send: FSInputFile = FSInputFile("data/all_teachers.txt")
        await callback_bt.message.answer_document(document=file_to_send)

    await callback_bt.answer("Вы выбрали кнопку {0}".format(callback_bt.data))