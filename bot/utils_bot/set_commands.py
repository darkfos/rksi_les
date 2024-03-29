from aiogram import types, Bot


# Установка списка команд в description бота
async def set_all_commands(bot: Bot):
    commands = [
        types.BotCommand(command="start", description="Запуск бота, выбор режима"),
        types.BotCommand(command="help", description="Поддержка, список доступных команд"),
        types.BotCommand(command="lessons_now", description="Получение списка пар на текущий день"),
        types.BotCommand(command="lessons_group", description="Вывод всех пар по названию группы"),
        types.BotCommand(command="prepod_name", description="Поиск пар преподавателя по фамилии"),
        types.BotCommand(command="groups", description="Вывод всех учебных групп"),
        types.BotCommand(command="prepods", description="Вывод всех преподавателей"),
    ]

    await bot.set_my_commands(commands=commands, scope=types.BotCommandScopeDefault())
