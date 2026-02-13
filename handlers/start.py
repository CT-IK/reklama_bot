from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from sqlalchemy.ext.asyncio import AsyncSession


from database.crud import get_or_create_user
from database.engine import get_session

start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message:types.Message):
    web_app_url = "https://ct-ik.github.io/reklama_web_app/"
    button = InlineKeyboardButton(text="Открыть приложение", web_app=WebAppInfo(url=web_app_url))
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])

    user_id = message.from_user.id
    # user = await get_or_create_user(session, user_id)
    async with get_session() as session:
        user = await get_or_create_user(session, user_id)
        if user:
            await message.answer(reply_markup=keyboard, text="Ваш Telegram ID записан в базу данных! Чтобы увидеть FAQ, откройте мини-приложение: ")
        else:
            await message.answer(reply_markup=keyboard,text="Вы уже зарегистрированы! Чтобы увидеть FAQ, откройте мини-приложение: ")
