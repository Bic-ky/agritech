# Generated by Django 4.2.1 on 2023-05-16 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0019_alter_project_farm_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
    ]
