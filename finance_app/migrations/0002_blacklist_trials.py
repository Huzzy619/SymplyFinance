# Generated by Django 4.2.2 on 2023-06-30 10:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("finance_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="blacklist",
            name="trials",
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
