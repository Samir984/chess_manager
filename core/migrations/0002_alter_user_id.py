# Generated by Django 5.1.5 on 2025-01-30 08:40

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
