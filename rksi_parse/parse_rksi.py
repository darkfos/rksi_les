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


async def parse_lessons_for_student(name_group: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(url_mobile, data={"group": name_group, "stt": "Показать!"}) as response:
            read_file = await aiohttp.StreamReader.read(response.content)
            soup = BeautifulSoup(read_file, "html.parser")
            all_data = str(soup.find("body"))
            test_re = re.findall(r"<h3>.+<br/>&?", all_data)
            data_with_for_split = re.findall(r"<b>.+<hr/><b>", test_re[0])
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

            print(data_with_for_split)
            print(unique_algorithm)