# Generated by Django 4.1.2 on 2023-01-30 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0020_alter_suborder_cart_items"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="comment",
            field=models.TextField(null=True),
        ),
    ]
