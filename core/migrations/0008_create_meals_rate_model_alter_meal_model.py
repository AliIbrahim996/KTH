# Generated by Django 4.1.2 on 2022-12-25 14:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_alter_cartitem_cart"),
    ]

    operations = [
        migrations.AddField(
            model_name="meal",
            name="delivery",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="meal",
            name="pickup",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="meal",
            name="pre_order",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="MealsRating",
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
                    "stars",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
                ("feedback", models.TextField(max_length=500, null=True)),
                (
                    "meal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.meal"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "meal")},
            },
        ),
    ]
