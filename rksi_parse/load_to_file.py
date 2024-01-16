import json

async def load_to_json(data_dict_lessons: dict) -> None:
    with open("data/lessons_schedule.json", "w") as js_write:
        json.dump(data_dict_lessons, js_write, indent=4, ensure_ascii=False)

async def loat_prepods_in_file(data_teachers: list) -> None:
    all_teachers: str = ""
    for teacher in data_teachers:
        all_teachers += teacher + "\n"

    with open("data/all_teachers.txt", "w", encoding="UTF-8") as wr_t:
        wr_t.write(all_teachers)
