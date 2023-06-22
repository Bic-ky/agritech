# Generated by Django 4.0.3 on 2023-06-18 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0010_remove_vendor_vendor_name'),
        ('orders', '0008_alter_order_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='vendors',
            field=models.ManyToManyField(blank=True, to='vendor.vendor'),
        ),
    ]
