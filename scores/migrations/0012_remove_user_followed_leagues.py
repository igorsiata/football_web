# Generated by Django 5.1.2 on 2024-11-21 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0011_match_unique_match'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followed_leagues',
        ),
    ]
