# Generated by Django 4.2.1 on 2023-06-11 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_order_inv_adr_order_inv_city_order_inv_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='rec_email',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='rec_email_other',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='rec_email_owner',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
