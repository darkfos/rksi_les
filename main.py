import asyncio

from rksi_parse import parse_lessons_for_student

if __name__ == "__main__":
    parse_rksi = asyncio.get_event_loop()
    parse_rksi.run_until_complete(parse_lessons_for_student("ИС-33"))
