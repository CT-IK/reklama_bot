import asyncio
from aiogram.fsm.state import State
from aiogram import F, Router, Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, User
from aiogram.fsm.state import StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import get_session
from config import BOT_TOKEN


brdcst_router = Router()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
# admins_list = ['2131378607', '1426715924']
admins_list = ['1426715924']


async def get_all_users(session):
    stmt = select(User.telegram_id)
    result = await session.execute(stmt)
    users = [row[0] for row in result.fetchall()]
    return users

class Message_maker(StatesGroup):
    content = State()
    ready_to_send = State()


@brdcst_router.message(Command("broadcast_534"))
async def add_content(message:types.Message, state:FSMContext):
    await message.answer("Введите текст сообщения: ")
    await state.set_state(Message_maker.content)

@brdcst_router.message(Message_maker.content, F.text)
async def image_settings(message:types.Message, state:FSMContext):
    await state.update_data(content=message.text)
    await message.answer("Сообщение сохранено!")
    await state.set_state(Message_maker.ready_to_send)

@brdcst_router.message(Message_maker.content)
async def image_settings(message:types.Message, state:FSMContext):
    await message.answer("Вы ввели данные неверно, введите сообщение для рассылки!")

# @start_router.message(StateFilter('waiting_for_img_reply'), F.text)
# async def image_answer(message:types.Message, state:FSMContext):
#     ans = str(message.text)
#     while True:
#         if ans == 'Да' or ans == 'да':
#             await message.answer("Загрузите изображение: ")
#             await state.set_state(Message_maker.image)
#             break
#         if ans == 'нет' or ans == 'Нет':
#             await state.set_state(Message_maker.image)
#             break
#         else:
#             await message.answer("Ох, кажется, вы введи что-то не то! Ответьте 'да' или 'нет'.")
#             continue

# @start_router.message(StateFilter('waiting_for_img_reply'))
# async def image_answer(message:types.Message, state:FSMContext):
#     await message.answer("Вы ввели данные неверно, введите сообщение для рассылки!")

# @start_router.message(Message_maker.image, F.photo)
# async def add_image_etc(message:types.Message, state:FSMContext):
#     await state.update_data(image=message.photo[-1].file_id)
#     await message.answer("Сообщение создано!")
#     data = await state.get_data()
#     await message.answer(str(data))
#     await state.set_state("ready_to_send")
    
# @start_router.message(Message_maker.image)
# async def add_image_etc(message:types.Message, state:FSMContext):
#     await message.answer("Вы ввели данные неверно, введите сообщение для рассылки!")

        
@brdcst_router.message(Message_maker.ready_to_send)
async def broadcast_cmd(message:types.Message, session:AsyncSession, state:FSMContext):
    user_id = message.from_user.id
    message_for_users = state.get_data()
    
    if str(user_id) not in admins_list:
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
    await state.clear()