import aiohttp
import config
import re


from bs4 import BeautifulSoup

from rksi_parse.files_wr.load_to_file import load_to_json

url = config.URL_RKSI_PREPODS
url_mobile = config.URL_RKSI_MOBILE


# Парсинг - получение списка преподавателей
async def parse_teachers() -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            read_file = await aiohttp.StreamReader.read(response.content)
            soup = BeautifulSoup(read_file, "html.parser")

            all_teachers = soup.find("select", id="teacher")
            all_teachers_list: list = list()

            for i in all_teachers:
                all_teachers_list.append(
                    i.text
                )

            return all_teachers_list


# Парсинг - получение списка учебных групп
async def all_groups() -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            read_file = await aiohttp.StreamReader.read(response.content)
            soup = BeautifulSoup(read_file, "html.parser")

            all_groups_req = soup.find("select", id="group")
            all_groups_lst: list = [group.text for group in all_groups_req]

            return all_groups_lst


# Парсинг - получение расписания всех пар для студентов
async def parse_lessons_for_student(name_group: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url_mobile, data={"group": name_group, "stt": "Показать!"}) as response:
            read_file = await aiohttp.StreamReader.read(response.content)
            soup = BeautifulSoup(read_file, "html.parser")
            all_data = str(soup.find("body"))

            result: dict = await process_str_lessons(all_data)
            await load_to_json(result, frm="student")

            return result


# Парсинг - получения раписания всех пар для преподавателей
async def parse_lessons_for_teachers(name_teacher: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url_mobile, data={"teacher": name_teacher, "stp": "Показать!"}) as response:
            read_file = await aiohttp.StreamReader.read(response.content)
            soup = BeautifulSoup(read_file, "html.parser")
            all_data = str(soup.find("body"))
            result: dict = await process_str_lessons(all_data)
            await load_to_json(result, frm="teacher")

            return result


# Метод для обработки HTML страницы, получения актуальных данных
async def process_str_lessons(data_str: str) -> dict:
    test_re = re.findall(r"<h3>.+<p><a>?", data_str)
    data_with_for_split = re.findall(r"<b>.+$", test_re[0])

    unique_algorithm: list = list()

    new_word = ""
    for word in data_with_for_split[0]:
        if word in "<b>pr":
            new_word += ""
        elif word == "/":
            if len(new_word) > 1:
                unique_algorithm.append(new_word)
            new_word = ""
        elif word == "h":
            unique_algorithm.append("\n")
        else:
            new_word += word

    lessons: dict = dict()

    lst: list = list()
    month: list = ["январ", "феврал", "март", "апрел", "мая", "июн", "июл", "август", "сентябр", "октябр", "ноябр", "декабр"]

    copy_name_d: str = ""
    for info in unique_algorithm:
        if any([m in info.strip() for m in month]):
            name_key_d = info.strip()
            if name_key_d != copy_name_d and name_key_d != "" and copy_name_d != "":
                lessons[copy_name_d] = lst
                lst = list()
            copy_name_d = info.strip()
        if len(info) > 1:
            lst.append(info.strip())

    return lessons