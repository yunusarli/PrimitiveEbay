# Generated by Django 3.1.8 on 2021-06-04 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_bids'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='price',
            field=models.PositiveIntegerField(default=10),
            preserve_default=False,
        ),
    ]
