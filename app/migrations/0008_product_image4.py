# Generated by Django 3.2.2 on 2021-05-14 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20210514_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image4',
            field=models.ImageField(default='', upload_to='image/'),
        ),
    ]
