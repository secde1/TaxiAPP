from sql_app.database import Base

from sqlalchemy import Column, Integer, String, Boolean

Base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=True)  # телефон необязательный
    email = Column(String, unique=True, index=True, nullable=True)  # почта необязательная
    hashed_password = Column(String, nullable=False)
    language = Column(String, default="russian")
    notifications_enabled = Column(Boolean, default=True)  # По умолчанию уведомления включены

    def __repr__(self):
        return f"<User(email='{self.email}', phone='{self.phone}')>"
# Модели базы данных (User): эти модели относятся к базе данных и должны быть в users.py,
# так как они отражают структуру таблиц и будут использоваться SQLAlchemy для взаимодействия с базой данных.
