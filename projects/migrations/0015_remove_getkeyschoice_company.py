# Generated by Django 4.2.1 on 2023-06-11 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_getkeyschoice_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='getkeyschoice',
            name='company',
        ),
    ]
