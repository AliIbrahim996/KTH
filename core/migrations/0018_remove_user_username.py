# Generated by Django 4.1.2 on 2023-01-28 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0017_remove_user_first_name_remove_user_last_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="username",
        ),
    ]
