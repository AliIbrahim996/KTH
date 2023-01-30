# Generated by Django 4.1.2 on 2023-01-31 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0022_orderrating"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="location",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.location",
            ),
        ),
    ]
