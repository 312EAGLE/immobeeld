# Generated by Django 4.2.1 on 2023-05-28 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='photography',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='property',
            name='photography_360',
            field=models.BooleanField(default=False),
        ),
    ]
