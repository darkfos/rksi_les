import emoji

from typing import List


# Текст для команды "help"
help_text = ("Привет! Я бот, который выводит данные о парах учебного заведения - РКСИ\n\n" \
             "🎯 <u>Мой перечень команд:</u>\n\n" \
             "🔥 <b>/start</b> - Старт бота, выбор режима\n" \
             "🔥 <b>/help</b> - Вывода списка команд\n" \
             "🔥 <b>/prepods</b> - Вывод всех преподавателей\n" \
             "🔥 <b>/prepod_name</b> - Пары преподавателя по фамилии\n" \
             "🔥 <b>/lessons_group</b> - Вывод всех пар по названию группы\n" \
             "🔥 <b>/lessons_now</b> - Вывод всех пар на текущий день\n" \
             "\n\n🔥 Так же я могу обрабатывать и простые сообщения!" \
             " Просто напиши название своей группы или инициалы преподавателя, а" \
             " я найду нужные пары!"
             )


# Текст для команды "start"
start_text = ("👋 Привет! Я бот помощник по расписанию <b>РКСИ</b>\n" \
              "Выбери нужный тебе пункт меню")


# Метод для генерации списка всех преподавателей в текстовом формате
async def get_all_teachers(lst_teachers: List) -> str:

    all_teachers: str = ""

    for teacher in lst_teachers:
        all_teachers += emoji.emojize(":man_teacher: {0}\n".format(teacher), language="en")

    return all_teachers


# Метод для генерации списка всех учебных групп в текстовом формате
async def get_all_groups(lst_groups: List) -> str:

    all_grp: str = ""

    for group in lst_groups:
        all_grp += emoji.emojize(":books: {}".format(group), language="en") + "\n"

    return all_grp