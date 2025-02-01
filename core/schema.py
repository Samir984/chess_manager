from ninja import Schema
from pydantic import EmailStr


class RegisterUserSchema(Schema):
    email: EmailStr
    first_name: str
    last_name: str
    image: str | None


class UserSchema(Schema):
    user_id: str
    email: EmailStr
    first_name: str
    last_name: str
    image: str | None


class ReportSchema(Schema):
    user_id: str
    title: str
    description: str


class GenericSchema(Schema):
    detail: str
