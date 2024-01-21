from aiogram.filters import BaseFilter
from aiogram import types

class TeacherData(BaseFilter):
    """
        Фильтр для проверки нажатия на кнопку для преподавателей
    """
    async def __call__(self, callback_data: types.CallbackQuery) -> bool:
        if callback_data.data.endswith("_btn"):
            return True
        return False
