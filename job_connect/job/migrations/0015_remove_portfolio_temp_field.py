# Generated by Django 5.1.1 on 2024-09-28 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0014_portfolio_temp_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='temp_field',
        ),
    ]
