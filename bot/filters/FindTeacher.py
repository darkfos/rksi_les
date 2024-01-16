from aiogram.filters import BaseFilter
from aiogram import types

from typing import List

from rksi_parse import parse_teachers

class FindTeacherName(BaseFilter):

    async def __call__(self, message: types.Message) -> bool:
        all_teachers: List = await parse_teachers()
        find_teacher_in_lst = any(message.text in teacher for teacher in all_teachers)
        
        return find_teacher_in_lst