from pydantic import BaseModel


class SupportMessageSchema(BaseModel):
    phone: str
    message: str
