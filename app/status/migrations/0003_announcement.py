# Generated by Django 4.2.3 on 2024-09-03 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("status", "0002_rename_user_gasoline_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Announcement",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=100)),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
