# Generated by Django 4.1.8 on 2023-05-12 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("halls", "0004_hallfavorite"),
        ("orders", "0003_alter_order_ordered_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="hall",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="halls.hall",
            ),
        ),
    ]
