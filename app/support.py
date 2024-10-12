import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from crud import crud
from sql_app.database import get_async_session
from schemas import SupportMessageSchema

router = APIRouter()
logging.basicConfig(level=logging.INFO)


# Эндпоинт для отправки сообщения в службу поддержки
@router.post("/support")
async def send_support_message(message: SupportMessageSchema, session: AsyncSession = Depends(get_async_session)):
    db_user = await crud.get_user_by_phone(message.phone)
    if not db_user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    # Здесь можно реализовать логику отправки сообщения в службу поддержки
    # Например, сохраняем сообщение в базе данных или отправляем на почту
    logging.info(f"Сообщение от пользователя {message.phone}: {message.message}")

    return {"message": "Ваше сообщение отправлено в службу поддержки."}
