# Generated by Django 4.0.3 on 2023-06-07 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_rename_is_superadmin_user_is_superuser_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='verification_method',
        ),
    ]
