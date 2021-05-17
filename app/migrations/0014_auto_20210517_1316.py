# Generated by Django 3.2.2 on 2021-05-17 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20210517_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Jeans', 'Jeans'), ('T-shirts', 'T-shirts'), ('Chino', 'Chino'), ('Pants', 'Pants'), ('Trousers', 'Trousers'), ('Shirts', 'Shirts'), ('Winters', 'Winters'), ('Shorts', 'Shorts'), ('Socks', 'Socks'), ('Belt', 'Belt'), ('Wallet', 'Wallet'), ('Shoes', 'Shoes'), ('Mask', 'Mask'), ('other_accessories', 'other_accessories')], default='', max_length=256),
        ),
        migrations.AddField(
            model_name='product',
            name='main_class',
            field=models.CharField(choices=[('Men', 'Men'), ('Women', 'Women'), ('Both', 'Both')], default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='product',
            name='size_available',
            field=models.CharField(default='', help_text='<small style="color:red;font-size:10px;">Please enter multiple size seperated by comma for ex: S,XL,XXL,XXXL</small>', max_length=256),
        ),
    ]