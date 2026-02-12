from aiogram import Bot, types, Router
from aiogram.filters import Command

from sqlalchemy.ext.asyncio import AsyncSession

command_router = Router()

@command_router.message(Command('user_id'))
async def get_user_id_cmd(message:types.Message):
    user_id = message.from_user.id
    await message.answer(str(user_id))