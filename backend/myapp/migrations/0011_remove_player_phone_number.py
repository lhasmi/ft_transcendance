# Generated by Django 5.0.4 on 2024-05-20 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_player_phone_number_player_secret_key_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='phone_number',
        ),
    ]
