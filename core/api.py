from typing import Optional
from uuid import UUID

from django.db import transaction
from django_ratelimit.decorators import ratelimit # type: ignore
from django.http.request import HttpRequest
from ninja import NinjaAPI, Form, File
from ninja.files import UploadedFile
from ninja import Router

from .models import User
from .models import Match
from .models import Profile



from .models import Report
from .schema import GenericSchema
from .schema import RegisterUserSchema
from .schema import ReportSchema
from .schema import UserSchema
from .schema import MatchCreateSchema,MatchUpdateSchema
from .security import TokenAuth
from .utils import handle_upload_to_cloudinary

token_auth = TokenAuth()

api = NinjaAPI(docs_url="/docs/", auth=token_auth)
users = Router()
matches = Router()


reports = Router()


api.add_router("/users/", users, tags=["users"])
api.add_router("/matches/", matches, tags=["matches"])
api.add_router("/reports/", reports, tags=["reports"])


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
            user_id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            image=user.image,
        )
    else:
        return 404, GenericSchema(detail="User doen't exits.")


@users.post("/register/", response={201: GenericSchema})
def register(request: HttpRequest, data: RegisterUserSchema):
    user, created = User.objects.get_or_create(
        email=data.email,
        defaults={
            "first_name": data.first_name,
            "last_name": data.last_name,
            "image": data.image,
        },
    )

    if created:
        # create profile also
        Profile.objects.create(user=user)
        return 201, GenericSchema(detail="User Create Successfully")

    return 201, GenericSchema(detail="User already exits.")

@matches.post("/", response={201: GenericSchema, 400: GenericSchema})
def create_match(request: HttpRequest, data: MatchCreateSchema):
    print(data)
    try:
        with transaction.atomic():
            Match.objects.create(
                id=data.game_id,
                player_white_id=data.player_white,
                player_black_id=data.player_black,
                is_bet=data.is_bet,
                bet_amount=data.bet_amount
            )

            players = User.objects.filter(id__in=[data.player_white, data.player_black]).select_related('profile')

            for player in players:
                player.profile.no_of_games_played += 1
                player.profile.save(update_fields=['no_of_games_played'])

        return 201, GenericSchema(detail="Match recorded successfully")

    except User.DoesNotExist:
        print("Error: One or both players do not exist.")
        return 400, GenericSchema(detail="One or both players do not exist.")

    except Exception as e:
        print("Error occurred: ", e)
        return 400, GenericSchema(detail="Something went wrong.")
    

@matches.patch("/",response={201:GenericSchema,400:GenericSchema})
def create_match(request:HttpRequest,data:MatchUpdateSchema):
    print(data,"enter")
    match=Match.objects.filter(id=data.game_id).first()
    print(match,"match")
    if match is None:
        return GenericSchema(detail="GameId doesn't exits.")
    if match.is_completed:
         return 400, GenericSchema(detail="Match is already completed.")
    try:
        players = User.objects.filter(id__in=[match.player_white_id, match.player_black_id]).select_related('profile')

        if match.is_bet and match.is_completed:
            pass   # handel bat related think
        
        if data.is_completed and data.winner_player:
            print("inside complete")
            match.is_completed = True
            match.winner_player_id = data.winner_player
            match.save()

            for player in players:
                print(player)
                if str(player.id) == str(data.winner_player):
                    print(player.first_name,"won")
                    player.profile.update_point(10)  # Winner gains 10 points
                else: 
                    print(player.first_name,"lose")
                    player.profile.update_point(-10)  # Loser loses 10 points
        
        elif data.is_completed and data.is_draw:
            print("inside draw")
            match.is_completed = True
            match.is_draw = True
            match.save()
        
        elif data.is_quit and data.quitter_player:
            print("inside quite")
            match.is_quit = True
            match.quitter_player_id = data.quitter_player
            match.save()




        return 201, GenericSchema(detail="Match updated successfully.")

    except Exception as e:
        print("Error occurred: ", e)
        return 400, GenericSchema(detail="Something went wrong.")    


@reports.post("/", response={201: GenericSchema, 400: GenericSchema}, auth=None)
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
