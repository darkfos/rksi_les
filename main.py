import asyncio
import logging
from bot import start_bot

from rksi_parse import parse_lessons_for_student

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_bot())