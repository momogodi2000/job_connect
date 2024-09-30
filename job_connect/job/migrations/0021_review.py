# Generated by Django 5.1.1 on 2024-09-29 00:38

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0020_portfolio_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=255)),
                ('client_email', models.EmailField(max_length=254)),
                ('comment', models.TextField()),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('expert', models.ForeignKey(limit_choices_to={'role': 'expert'}, on_delete=django.db.models.deletion.CASCADE, related_name='expert_reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
