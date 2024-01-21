from aiogram import types
from aiogram.filters import BaseFilter


class FilterChoice(BaseFilter):
    """
        Фильтр для поля меню
    """
    async def __call__(self, message: types.Message) -> bool:
        if message.text.title() in ("🎓 Студент", "🧙 Преподаватель"):
            return True
        return False

