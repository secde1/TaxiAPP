from pydantic import BaseModel


class UserPreferencesSchema(BaseModel):
    language: str  # 'uzbek' or 'russian'
    notifications_enabled: bool
