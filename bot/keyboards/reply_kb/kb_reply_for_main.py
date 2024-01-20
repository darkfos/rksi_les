from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

async def get_start_bt() -> ReplyKeyboardMarkup:

    kb = [
        [
            KeyboardButton(text="🎓 Студент"),
            KeyboardButton(text="🧙 Преподаватель")
        ]
    ]

    alL_kb_start: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выбор режима"
    )

    return alL_kb_start