from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBaseSchema(BaseModel):
    phone: Optional[str] = Field(pattern=r'^\+998\d{9}$',
                                 default=None)  # телефон не обязателен, но если есть — проверка
    email: Optional[EmailStr] = None  # почта не обязательна

    class Config:
        from_attributes = True


class UserCreateSchema(UserBaseSchema):
    first_name: str
    last_name: str
    password: str

    class Config:
        from_attributes = True


class UserLoginSchema(UserBaseSchema):
    password: str


class UserUpdateSchema(UserBaseSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        from_attributes = True


class VerifyCodeSchema(BaseModel):
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    code: int


class TokenSchema(BaseModel):
    access_token: str
    token_type: str

# Модели Pydantic (UserBase, UserCreate, UserLogin, Token): оставить в main.py
# или в отдельном файле, например, users.py. Эти модели нужны для валидации данных при регистрации, входе и возврате токенов.
