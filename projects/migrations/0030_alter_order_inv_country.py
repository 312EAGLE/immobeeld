# Generated by Django 4.2.1 on 2023-06-12 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0029_rename_country_invcountry_inv_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='inv_country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]