# Generated by Django 4.1.8 on 2023-05-19 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("halls", "0011_alter_hall_event_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hall",
            name="view_count",
            field=models.BigIntegerField(default=0),
        ),
    ]