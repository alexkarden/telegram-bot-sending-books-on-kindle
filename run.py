import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from database import init_db
from handlers import router


load_dotenv()
bot = Bot(token=os.getenv("TOKEN_TG"))
dp = Dispatcher()


async def main():
    await init_db()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.WARNING,
        filename="py_log.log",
        filemode="w",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.warning("Exit")
