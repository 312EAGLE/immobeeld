# Generated by Django 4.2.1 on 2023-06-12 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0027_order_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvCountry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='inv_country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.invcountry'),
        ),
    ]
