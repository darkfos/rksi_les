import json

import aiohttp
import config
import requests
import re


from bs4 import BeautifulSoup

url = config.URL_RKSI_PREPODS
url_mobile = config.URL_RKSI_MOBILE

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


async def all_groups() -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            read_file = await aiohttp.StreamReader.read(response.content)
            soup = BeautifulSoup(read_file, "html.parser")

            all_groups_req = soup.find("select", id="group")
            all_groups_lst: list = [group.text for group in all_groups_req]

            return all_groups_lst


async def parse_lessons_for_student(name_group: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url_mobile, data={"group": name_group, "stt": "Показать!"}) as response:
            read_file = await aiohttp.StreamReader.read(response.content)
            soup = BeautifulSoup(read_file, "html.parser")
            all_data = str(soup.find("body"))

            result: dict = await process_str_lessons(all_data)
            await load_to_json(result)

            return result


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
    dct_to_add: dict = dict()

    count_day: int = 0
    numeric_data: int = 0
    for day_lesson in unique_algorithm:
        if day_lesson == "\n":
            lessons[count_day] = dct_to_add
            dct_to_add = dict()
            numeric_data = 0
            count_day += 1
        else:
            if numeric_data == 0:
                dct_to_add["День"] = day_lesson.strip()
            else:
                dct_to_add[str(numeric_data)] = day_lesson.strip()

            numeric_data += 1

    return lessons