# Generated by Django 3.2.23 on 2023-12-04 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('My_Store', '0007_cartitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
    ]
