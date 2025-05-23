# Generated by Django 5.2 on 2025-04-22 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Conference",
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
                ("name", models.CharField(max_length=255)),
                ("year", models.IntegerField()),
                ("location", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Talk",
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
                ("title", models.CharField(max_length=255)),
                ("speaker", models.CharField(max_length=255)),
                ("description", models.TextField()),
            ],
        ),
    ]
