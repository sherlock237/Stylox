# Generated by Django 3.2.3 on 2021-05-22 11:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_order_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='order_id',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
