# Generated by Django 4.1.8 on 2023-05-13 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("halls", "0004_hallfavorite"),
    ]

    operations = [
        migrations.RenameField(
            model_name="hall",
            old_name="user",
            new_name="owner",
        ),
    ]
