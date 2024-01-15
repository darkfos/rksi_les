import asyncio
import aiohttp
import config


from bs4 import BeautifulSoup


async def parse_teachers():
    url = config.URL_RKSI_PREPODS
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
            print(all_teachers_list)
