# Generated by Django 4.0.3 on 2023-05-08 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='pin_code',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
