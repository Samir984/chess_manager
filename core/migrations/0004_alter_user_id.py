# Generated by Django 5.1.5 on 2025-01-30 08:49

import uuid

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
