from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends, APIRouter

import core
from crud import crud
from models import User
from sql_app import get_async_session
from services import send_email_verification_code, client, TWILIO_PHONE_NUMBER
from schemas import UserCreateSchema, TokenSchema, UserLoginSchema, VerifyCodeSchema
from core import generate_verification_code, hash_password, verify_password, create_access_token

router = APIRouter()
verification_codes = {}


# Отправка кода подтверждения
@router.post("/auth/send-code")
async def send_verification_code(
        phone: Optional[str] = None, email: Optional[str] = None
):
    """
    Пользователь передает либо телефон, либо email для отправки кода.
    """
    if not phone and not email:
        raise HTTPException(
            status_code=400, detail="Необходимо указать либо телефон, либо электронную почту."
        )

    code = core.utils.generate_verification_code()  # функция генерации кода, например, 6 цифр
    print('code---------------------------------->', code)
    # Отправляем код на телефон
    if phone:
        print('phone----------------------------------------->', phone)
        verification_codes[phone] = code
        try:
            print('client--------------------------->', client)
            print(f"Отправка SMS на {phone} с кодом {code}")
            client.messages.create(
                body=f"Ваш код подтверждения: {code}",
                from_=TWILIO_PHONE_NUMBER,
                to=phone
            )
            return {"message": "Код подтверждения отправлен на телефон."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка отправки SMS: {e}")

    # Отправляем код на email
    if email:
        verification_codes[email] = code
        try:
            # Пример отправки через SMTP:
            send_email_verification_code(email, code)
            return {"message": "Код подтверждения отправлен на почту."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка отправки кода на почту: {e}")


# Проверка кода подтверждения
@router.post("/auth/verify-code")
async def verify_code(payload: VerifyCodeSchema):
    """
    Пользователь подтверждает код, отправленный на телефон или почту.
    """
    if payload.phone and verification_codes.get(payload.phone) == payload.code:
        del verification_codes[payload.phone]  # Удаляем код после успешной верификации
        return {"message": "Код подтвержден. Теперь можно завершить регистрацию."}
    elif payload.email and verification_codes.get(payload.email) == payload.code:
        del verification_codes[payload.email]  # Удаляем код после успешной верификации
        return {"message": "Код подтвержден. Теперь можно завершить регистрацию."}
    else:
        raise HTTPException(status_code=400, detail="Неверный код подтверждения.")


@router.post("/signup", response_model=TokenSchema)
async def signup(user: UserCreateSchema, session: AsyncSession = Depends(get_async_session)):
    """
    Завершение регистрации: пользователь вводит имя, фамилию и пароль после подтверждения номера телефона или почты.
    """
    if not user.phone and not user.email:
        raise HTTPException(status_code=400, detail="Нужно указать либо телефон, либо почту.")

    db_user = None
    if user.email:
        db_user = await crud.get_user_by_email(session, user.email)
    elif user.phone:
        db_user = await crud.get_user_by_phone(session, user.phone)

    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь с такими данными уже существует.")

    hashed_password = hash_password(user.password)  # Хешируем пароль
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        email=user.email,
        hashed_password=hashed_password
    )

    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при регистрации")

    # Создаем JWT-токен после успешной регистрации
    access_token = create_access_token(data={"sub": new_user.email if new_user.email else new_user.phone})
    return {"access_token": access_token, "token_type": "Bearer"}


# Логика для входа пользователя
@router.post("/login", response_model=TokenSchema)
async def login(user: UserLoginSchema, session: AsyncSession = Depends(get_async_session)):
    """
    Пользователь может войти с номером телефона или электронной почтой и паролем.
    """
    if not user.phone and not user.email:
        raise HTTPException(status_code=400, detail="Необходимо указать либо телефон, либо электронную почту.")

    db_user = None
    if user.email:
        db_user = await crud.get_user_by_email(session, user.email)
    elif user.phone:
        db_user = await crud.get_user_by_phone(session, user.phone)

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail='Некорректный номер телефона, email или пароль')

    # Если пользователь прошел все проверки, выдаем токен
    access_token = create_access_token(data={'sub': user.email if user.email else user.phone})
    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post("/auth/reset-password")
async def reset_password(
        phone: Optional[str] = None,
        email: Optional[str] = None,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Отправка кода подтверждения для сброса пароля на телефон или электронную почту.
    """
    if not phone and not email:
        raise HTTPException(status_code=400, detail="Необходимо указать либо телефон, либо электронную почту.")

    code = generate_verification_code()  # Генерируем код

    # Отправляем код на телефон
    if phone:
        user = await crud.get_user_by_phone(session, phone)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден.")
        verification_codes[phone] = code
        client.messages.create(
            body=f"Ваш код для сброса пароля: {code}",
            from_=TWILIO_PHONE_NUMBER,
            to=phone
        )
        return {"message": "Код подтверждения отправлен на телефон."}

    # Отправляем код на email
    if email:
        user = await crud.get_user_by_email(session, email)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден.")
        verification_codes[email] = code
        send_email_verification_code(email, code)
        return {"message": "Код подтверждения отправлен на почту."}


@router.post("/auth/change-password")
async def change_password(
        payload: VerifyCodeSchema,
        new_password: str,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Изменение пароля после подтверждения кода.
    """
    if payload.phone and verification_codes.get(payload.phone) == payload.code:
        user = await crud.get_user_by_phone(session, payload.phone)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден.")

        user.hashed_password = hash_password(new_password)  # Хешируем новый пароль
        del verification_codes[payload.phone]  # Удаляем код после успешной верификации
        await session.commit()
        return {"message": "Пароль успешно изменен."}

    elif payload.email and verification_codes.get(payload.email) == payload.code:
        user = await crud.get_user_by_email(session, payload.email)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден.")

        user.hashed_password = hash_password(new_password)  # Хешируем новый пароль
        del verification_codes[payload.email]  # Удаляем код после успешной верификации
        await session.commit()
        return {"message": "Пароль успешно изменен."}

    raise HTTPException(status_code=400, detail="Неверный код подтверждения.")
