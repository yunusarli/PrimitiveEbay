# Generated by Django 3.1.8 on 2021-06-07 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_bids_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='user',
        ),
    ]
