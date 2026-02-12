from sqlalchemy import select

from .models import User


async def get_or_create_user(session, telegram_id: int):
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        new_user = User(telegram_id=telegram_id)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)  # Обновляем объект
        return new_user
    return user