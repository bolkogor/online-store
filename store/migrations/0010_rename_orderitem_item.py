# Generated by Django 4.1.4 on 2022-12-29 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_price'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderItem',
            new_name='Item',
        ),
    ]
