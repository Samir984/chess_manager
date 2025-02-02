from typing import Optional
from uuid import UUID

from django_ratelimit.decorators import ratelimit # type: ignore
from django.http.request import HttpRequest
from ninja import NinjaAPI, Form, File
from ninja.files import UploadedFile
from ninja import Router

from .models import User
from .models import Report
from .schema import GenericSchema
from .schema import RegisterUserSchema
from .schema import ReportSchema
from .schema import UserSchema
from .security import TokenAuth
from .utils import handle_upload_to_cloudinary

token_auth = TokenAuth()

api = NinjaAPI(docs_url="/docs/", auth=token_auth)
users = Router()
report = Router()


api.add_router("/users/", users, tags=["users"])
api.add_router("/reports/", report, tags=["reports"])


@users.get("/", response={200: UserSchema, 400: GenericSchema})
def get_user(
    request: HttpRequest,
    email: Optional[str] = None,
    user_id: Optional[UUID] = None,
):
    if not email and not user_id:
        return 400, GenericSchema(
            detail="Please provide either email or user_id."
        )
    if email:
        user = User.objects.filter(email=email).first()
    elif user_id:
        user = User.objects.filter(id=user_id).first()
    else:
        return 400, GenericSchema(
            detail="Please provide either email or user_id."
        )
    if user:
        return 200, UserSchema(
            user_id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            image=user.image,
        )
    else:
        return 404, GenericSchema(detail="User doen't exits.")


@users.post("/register/", response={201: GenericSchema})
def register(request: HttpRequest, data: RegisterUserSchema):
    _, created = User.objects.get_or_create(
        email=data.email,
        defaults={
            "first_name": data.first_name,
            "last_name": data.last_name,
            "image": data.image,
        },
    )

    if created:
        return 201, GenericSchema(detail="User Create Successfully")

    return 201, GenericSchema(detail="User already exits.")


@report.post("/", response={201: GenericSchema, 400: GenericSchema}, auth=None)
def create_report(
    request: HttpRequest,
    payload: Form[ReportSchema],
    image: Optional[UploadedFile] = File(None),  # type: ignore
):  
    
    public_id:str=""
    secure_url:str=""
    report = Report(
        user_id=payload.user_id,
        title=payload.title,
        description=payload.description,

    )
    try:
        if image:
            res=handle_upload_to_cloudinary(image)
            print(res["secure_url"])
            public_id=res["public_id"]
            secure_url=res["secure_url"]

        report.imageURL = secure_url
        report.public_id = public_id
        report.save()


    except Exception as e:
        print(e,"eee")
        return 400, GenericSchema(detail="Error, something went wrong, please try laterr")


    print(report)
    return 201, GenericSchema(detail="Report created successfully.")
