# Generated by Django 4.2 on 2023-06-15 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0022_alter_userprofile_state"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="facebook",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="instagram",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="linkedin",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="twitter",
            field=models.URLField(blank=True, null=True),
        ),
    ]
