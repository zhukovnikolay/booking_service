# Generated by Django 4.1.8 on 2023-04-25 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("halls", "0005_alter_hall_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="hall",
            name="view_count",
            field=models.IntegerField(default=0),
        ),
    ]
