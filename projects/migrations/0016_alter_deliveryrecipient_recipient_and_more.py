# Generated by Django 4.2.1 on 2023-06-11 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_remove_getkeyschoice_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryrecipient',
            name='recipient',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='invoicerecipient',
            name='recipient',
            field=models.CharField(max_length=50),
        ),
    ]
