# Generated by Django 3.1.5 on 2021-05-20 16:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_remove_order_placed_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='added_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
