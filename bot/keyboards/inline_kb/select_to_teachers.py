from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


async def sel_to_teachers() -> InlineKeyboardBuilder:
    keyboards_st = InlineKeyboardBuilder()
    keyboards_st.add(InlineKeyboardButton(text="Список", callback_data="list_btn"))
    keyboards_st.add(InlineKeyboardButton(text="Файл", callback_data="file_btn"))

    return keyboards_st.as_markup()