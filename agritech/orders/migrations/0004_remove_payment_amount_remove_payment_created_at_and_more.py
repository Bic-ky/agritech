# Generated by Django 4.2.1 on 2023-05-28 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_payment_status_delete_verification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='status',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='transaction_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
    ]
