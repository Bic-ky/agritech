# Generated by Django 4.0.3 on 2023-06-18 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0031_completedproject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='completedproject',
            name='description_title',
        ),
    ]
