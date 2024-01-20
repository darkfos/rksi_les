import asyncio
import csv

async def load_prepods_to_csv(lst_prepods: list) -> None:
    """
    Загружает данные о преподавателях в csv формат
    :param lst_prepods:
    :return:
    """

    with open("data/all_teachers.csv", "w", encoding="UTF-8") as f_csv:
        wr = csv.writer(f_csv, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(["Преподаватели"])
        for teacher in lst_prepods:
            wr.writerow([teacher])

async def load_groups_to_csv(lst_groups: list) -> None:
    """
    Загружает данные о группах в csv формат
    :param lst_groups:
    :return:
    """

    with open("data/all_groups.csv", "w", encoding="UTF-8") as f_csv:
        wr = csv.writer(f_csv, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow("Группы")
        for group in lst_groups:
            wr.writerow(
                [group]
            )