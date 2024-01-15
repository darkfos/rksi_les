import asyncio

from rksi_parse import parse_teachers

if __name__ == "__main__":
    parse_rksi = asyncio.get_event_loop()
    parse_rksi.run_until_complete(parse_teachers())
