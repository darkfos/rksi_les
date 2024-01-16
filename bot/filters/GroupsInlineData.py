from aiogram.filters import BaseFilter
from aiogram import types


class GroupsData(BaseFilter):
    async def __call__(self, callback_data: types.CallbackQuery) -> bool:
        if callback_data.data.endswith("_gbtn"):
            return True
        return False