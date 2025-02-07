import secrets
from decimal import Decimal 
import uuid
from typing import Any

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from .choices import Side

# from .validator import validate_file_size


def get_default_token():
    return secrets.token_hex(20)


# Custom User Manager
class CustomerUserManager(BaseUserManager): # type: ignore
    def create_user(self, email:str, password=None, **extra_fields:Any): # type: ignore
        if not email:
            raise ValueError("The Email field must be set ")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields) # type: ignore
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email:str, password=None, **extra_fields:Any): # type: ignore
        print("Create superuser custome manager running\n\n\n\n")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields) # type: ignore


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    image = models.URLField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomerUserManager() # type: ignore


    def save(self, *args:Any, **kwargs:dict[str, Any]):
        if not self.pk:
            super().save(*args, **kwargs) 
            Profile.objects.create(user=self)  
        else:
            super().save(*args, **kwargs)  


    def __str__(self):
        return self.get_full_name()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    no_of_games_played = models.PositiveIntegerField(default=0)
    coins = models.PositiveIntegerField(
        default=0,  
        validators=[MaxValueValidator(10000)]  
    )
    game_point = models.IntegerField(
        default=0 , validators=[MinValueValidator(0),MaxValueValidator(10000)]  
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_coins(self, money: int):
        """ update the coins in database  """
        if money > 0:
            self.coins += money
        elif money < 0:
            self.coins = max(0, self.coins - money) 
        self.save(update_fields=['coins'])

    
    def update_point(self, point: int):
        """ update the game_point in database  """
        if point > 0:
            self.game_point += point
        elif point < 0:
            self.game_point = max(0, self.game_point - point) 
        self.save(update_fields=['game_point'])

      

    def __str__(self):
        return f"{self.user.username} - ({self.game_point} pts)"


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    imageURL = models.URLField(null=True,blank=True)
    public_id = models.CharField(max_length=255,null=True,blank=True)
    is_solved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Match(models.Model):
    game_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    players = models.ManyToManyField(User, related_name='freematches') # type: ignore
    player_1 = models.CharField(max_length=1,choices=Side.choices)
    player_2 = models.CharField(max_length=1,choices=Side.choices)
    game_id = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    is_quit = models.BooleanField(default=False) 
    is_bet = models.BooleanField(default=False)
    bet_amount = models.DecimalField(default=Decimal("0.00"), max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
 

    def __str__(self):
        return f"FreeMatch {self.game_id}"

class MatchResult(models.Model):
    game_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    winner_player = models.ForeignKey(User,on_delete=models.CASCADE)
    winner_side = models.CharField(max_length=1,choices=Side.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    
    

class Token(models.Model):
    key = models.CharField(
        max_length=255, unique=True, default=get_default_token
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user}"
