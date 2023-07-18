# Generated by Django 4.2.1 on 2023-05-28 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_property_photography_property_photography_360'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='total_excl_vat',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='total_incl_vat',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
