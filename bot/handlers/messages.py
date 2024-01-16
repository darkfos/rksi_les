from aiogram import types, Router

from bot.filters import FindTeacherName
msg_router = Router()

@msg_router.message(FindTeacherName())
async def new_msg(message: types.Message):
    await message.answer("Преподаватель был найден в БД")


@msg_router.message()
async def processing_other_messages(message: types.Message):
    await message.answer("Не могу распознать ваш текст.\nОжидается команда или инициалы преподавателя")