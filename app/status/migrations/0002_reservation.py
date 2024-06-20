# Generated by Django 4.2.3 on 2024-06-20 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("status", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reservation",
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
                ("user", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=100)),
                ("start_date", models.DateField()),
                ("duration", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
