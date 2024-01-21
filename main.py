import asyncio
import logging

from bot import start_bot


# Запуск проекта
if __name__ == "__main__":

    # Подключение логирования
    logging.basicConfig(level=logging.INFO)

    # Асинхронный запуск бота
    asyncio.run(start_bot())