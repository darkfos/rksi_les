from aiogram import types
from aiogram.filters import BaseFilter


class GroupsData(BaseFilter):
    """
        Фильтр для проверки имени группы
    """
    async def __call__(self, callback_data: types.CallbackQuery) -> bool:
        if callback_data.data.endswith("_gbtn"):
            return True
        return False