# Generated by Django 4.2.3 on 2023-07-21 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_alter_customer_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'permissions': [{'view_history', 'can_view_history'}]},
        ),
    ]
