# Generated by Django 4.2.3 on 2024-06-21 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("status", "0005_alter_reservation_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Gasoline",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("user", models.CharField(max_length=100)),
                ("price", models.IntegerField()),
                ("comment", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]