from aiogram.filters import BaseFilter
from aiogram import types


class FilterChoice(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if message.text.title() in ("Студент", "Преподаватель"):
            return True
        return False

