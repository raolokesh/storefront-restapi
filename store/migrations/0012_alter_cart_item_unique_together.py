# Generated by Django 4.2.3 on 2023-07-15 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_cart_item_cart'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cart_item',
            unique_together={('cart', 'product')},
        ),
    ]
