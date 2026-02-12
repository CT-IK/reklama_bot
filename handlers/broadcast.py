import asyncio
from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import get_session
from config import BOT_TOKEN

start_router = Router()
bot = Bot(token=BOT_TOKEN)


async def get_all_users(session):
    stmt = select(User.telegram_id)
    result = await session.execute(stmt)
    users = [row[0] for row in result.fetchall()]
    return users


@start_router.message(Command('broadcast_354'))
async def broadcast_cmd(message: Message, session: AsyncSession):
    user_id = message.from_user.id
    message_for_users = ""  # этот момент сделать через машину состояний

    if user_id != 2131378607:
        await message.reply('Извините, вы не админ!')
        return

    users = await get_all_users(session)

    sent_count = 0
    failed_count = 0

    for user_id in users:
        try:
            await bot.send_message(chat_id=user_id, text=message_for_users)
            sent_count += 1
        except Exception as e:
            await message.reply(f"Ошибка у {user_id} : {e}")
            failed_count += 1
        await asyncio.sleep(0.05)

    await message.reply(f'Рассылка завершена!\n\n'
                        f'Успешно разослано: {sent_count}\n'
                        f'Bad разослано: {failed_count}')