# Generated by Django 3.2.2 on 2021-05-11 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_product_size_available'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('banid', models.AutoField(primary_key=True, serialize=False)),
                ('image1', models.ImageField(default='', upload_to='image/')),
                ('image2', models.ImageField(default='', upload_to='image/')),
                ('image3', models.ImageField(default='', upload_to='image/')),
            ],
        ),
    ]
