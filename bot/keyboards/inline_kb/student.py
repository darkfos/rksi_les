from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


# Inline кнопки для получения расписания, создания и удаления щаблона поиска
async def get_student_choice_bt() -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="📑 Шаблон", callback_data="shablon_stbtn"))
    kb.row(InlineKeyboardButton(text="📑 Удалить шаблон", callback_data="del_shablon_stbtn"))
    kb.row(InlineKeyboardButton(text="✍🏼 Ручной ввод", callback_data="group_name_stbtn"))

    return kb.as_markup()