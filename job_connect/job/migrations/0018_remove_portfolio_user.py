# Generated by Django 5.1.1 on 2024-09-28 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0017_portfolio_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='user',
        ),
    ]
