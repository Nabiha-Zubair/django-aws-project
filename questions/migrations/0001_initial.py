# Generated by Django 5.0 on 2023-12-29 21:39

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("topic", "0002_alter_topic_options_alter_topic_title"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        max_length=255,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=3,
                                message="Title must be at least 3 characters long.",
                            )
                        ],
                    ),
                ),
                ("topics", models.ManyToManyField(to="topic.topic")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]