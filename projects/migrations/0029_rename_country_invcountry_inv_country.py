# Generated by Django 4.2.1 on 2023-06-12 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0028_invcountry_alter_order_inv_country'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invcountry',
            old_name='country',
            new_name='inv_country',
        ),
    ]
