from django.db import models

class Side(models.TextChoices):
    WHITE = ("W", "White")
    BLACK = ("B", "Black")


# class MatchStatus(models.TextChoices):
#     ACTIVE = ("ACTIVE", "Active")
#      = ("B", "Black")
