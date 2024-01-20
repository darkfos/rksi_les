import json

from bot.text import get_all_groups

async def load_to_json(data_dict_lessons: dict, frm: str) -> None:
    if frm == "teacher":
        data_file: str = "lessons_schedule_for_teachers.json"
    else:
        data_file: str = "lessons_schedule_for_students.json"

    print(data_file)

    with open(f"data/{data_file}", "w") as js_write:
        json.dump(data_dict_lessons, js_write, indent=4, ensure_ascii=False)

async def load_prepods_in_file(data_teachers: list) -> None:
    all_teachers: str = ""
    for teacher in data_teachers:
        all_teachers += teacher + "\n"

    with open("data/all_teachers.txt", "w", encoding="UTF-8") as wr_t:
        wr_t.write(all_teachers)


async def load_groups_in_file(data_groupds: list) -> None:
    all_grp = await get_all_groups(data_groupds)

    with open("data/all_groups.txt", "w", encoding="UTF-8") as gr_file:
        gr_file.write(all_grp)
