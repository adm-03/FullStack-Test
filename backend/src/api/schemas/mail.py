from pydantic import EmailStr, Field
from .base import BaseSchema




class MailSchema(BaseSchema):
    name: str = Field(
        ...,
        description="Имя пользователя",
        examples=["Иван"],
        min_length=2,
        max_length=50,
    )
    phone: str = Field(
        ...,
        pattern=r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\- ]?[0-9]{3}[\s\- ]?[0-9]{2}[\s\- ]?[0-9]{2}$",
        description="Номер телефона в формате +79991234567 или 89991234567",
        examples=["+79991234567"]
    )
    email: EmailStr = Field(
        ...,
        description="Почта пользователя (туда уйдет копия)",
        examples=["user@mail.ru"],
        max_length=50,
    )
    comment: str = Field(
        ...,
        description="Текст комментария/сообщения",
        examples=["Здравствуйте!"],
        min_length=5,
        max_length=500,
    )