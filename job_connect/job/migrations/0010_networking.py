# Generated by Django 5.1.1 on 2024-09-28 10:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0009_portfolio_age_portfolio_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Networking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('age', models.PositiveIntegerField()),
                ('resume', models.FileField(upload_to='resumes/')),
                ('social_media_gmail', models.URLField(blank=True, null=True)),
                ('social_media_facebook', models.URLField(blank=True, null=True)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.domain')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.specification')),
            ],
        ),
    ]
