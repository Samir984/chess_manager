from typing import Optional

from ninja import Schema,ModelSchema
from ninja.files import UploadedFile
from pydantic import EmailStr
from .models import Report



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


class ReportSchema(ModelSchema):
    user_id: str
    image: Optional[UploadedFile]  # Correct type annotation
    
    class Meta:
        model = Report
        fields = ['title', 'description', 'image']



class GenericSchema(Schema):
    detail: str
