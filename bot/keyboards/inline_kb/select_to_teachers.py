from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


async def sel_to_teachers() -> InlineKeyboardBuilder:
    keyboards_st = InlineKeyboardBuilder()
    keyboards_st.add(InlineKeyboardButton(text="📝 Список", callback_data="list_btn"))
    keyboards_st.add(InlineKeyboardButton(text="📄 Файл txt", callback_data="file_btn"))
    keyboards_st.add(InlineKeyboardButton(text="📁 Файл csv", callback_data="filecsv_btn"))

    return keyboards_st.as_markup()


async def sel_to_groups() -> InlineKeyboardBuilder:
    kb_gr = InlineKeyboardBuilder()
    kb_gr.add(InlineKeyboardButton(text="📝 Список", callback_data="list_gbtn"))
    kb_gr.add(InlineKeyboardButton(text="📄 Файл", callback_data="file_gbtn"))
    kb_gr.add(InlineKeyboardButton(text="📁 Файл csv", callback_data="filecsv_btn"))

    return kb_gr.as_markup()