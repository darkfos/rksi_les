from aiogram import types
from aiogram.filters import BaseFilter

from rksi_parse import parse_teachers

from typing import List


class FindTeacherName(BaseFilter):
    """
        Фильтр для проверки имени преподавателя
    """
    async def __call__(self, message: types.Message) -> bool:
        all_teachers: List = await parse_teachers()
        find_teacher_in_lst: bool = any([message.text.title() in teacher for teacher in all_teachers])
        return find_teacher_in_lst