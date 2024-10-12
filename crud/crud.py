from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.users import User


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    result = await session.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_user_by_phone(session: AsyncSession, phone: str) -> User:
    result = await session.execute(select(User).filter(User.phone == phone))
    return result.scalars().first()


async def get_user_by_id(session: AsyncSession, user_id: int):
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalars().first()
