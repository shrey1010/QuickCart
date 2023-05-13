# Generated by Django 4.1.5 on 2023-03-28 17:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0002_remove_user_tc_user_is_verified_user_otp"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_verified",
        ),
        migrations.RemoveField(
            model_name="user",
            name="otp",
        ),
        migrations.AddField(
            model_name="user",
            name="tc",
            field=models.BooleanField(default=False),
        ),
    ]