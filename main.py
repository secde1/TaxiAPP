from fastapi import FastAPI
from app import auth_router, support_router, preferences_router
app = FastAPI()

app.include_router(auth_router)
app.include_router(support_router)
app.include_router(preferences_router)

# Остальная часть вашего кода, например, настройки базы данных
