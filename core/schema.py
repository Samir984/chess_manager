from decimal import Decimal
from pydantic import Field
from typing import Optional

from uuid import UUID
from ninja import Schema,ModelSchema
from pydantic import EmailStr
from core import models


class RegisterUserSchema(Schema):
    email: EmailStr
    first_name: str
    last_name: str
    image: str | None


class UserSchema(Schema):
    user_id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    image: str | None


class ProfileSchema(ModelSchema):
    first_name: str = Field(..., alias="user.first_name")
    last_name: str = Field(..., alias="user.last_name")
    image_url: Optional[str] = Field(None, alias="user.image")  # Allow None values
    email: str = Field(..., alias="user.email")
    won_matches_count:int

    class Meta:
        model = models.Profile
        fields = ["user", "no_of_games_played", "coins", "game_point"]

    


class MatchCreateSchema(Schema):
    game_id:UUID
    is_bet: bool=False
    bet_amount:Decimal= Field(default=Decimal('0.00'), ge=Decimal('0.00'), le=Decimal('1000.00'))
    player_white:str
    player_black:str

class MatchUpdateSchema(Schema):
    game_id:UUID
    quitter_player:Optional[str]=None
    winner_player:Optional[str]=None
    unexpected_leaver_player:Optional[str]=None
    is_terminated:Optional[bool]=None
    is_quit:Optional[bool]=None
    is_completed:Optional[bool]=None
    is_draw:Optional[bool]=None
    is_timeout:Optional[bool]=None
    is_left:Optional[bool]=None

    




class ReportSchema(Schema):
    user_id: UUID
    title: str
    description: str


class GenericSchema(Schema):
    detail: str
