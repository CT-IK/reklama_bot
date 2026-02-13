import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.engine import create_db
from handlers.start import start_router
from handlers.user_id import command_router
from handlers.broadcast import brdcst_router
import database.models


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(command_router)
dp.include_router(brdcst_router)
# dp.include_router(db_router)


async def main():
    await create_db()  # Создаём таблицы, если их нет
    await dp.start_polling(bot)
    print("Бот запущен")

if __name__ == '__main__':
    asyncio.run(main())