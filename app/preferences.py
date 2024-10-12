from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from crud import crud
from sql_app.database import get_async_session
from schemas import UserPreferencesSchema

router = APIRouter()


# Эндпоинт для обновления предпочтений пользователя
@router.put("/auth/preferences")
async def update_user_preferences(preferences: UserPreferencesSchema, session: AsyncSession = Depends(get_async_session)):
    db_user = await crud.get_user_by_phone(preferences.phone)
    if not db_user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    db_user.language = preferences.language
    db_user.notifications_enabled = preferences.notifications_enabled
    await session.commit()
    return {"message": "Предпочтения успешно обновлены."}
