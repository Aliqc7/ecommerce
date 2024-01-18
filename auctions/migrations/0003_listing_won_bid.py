# Generated by Django 5.0.1 on 2024-01-18 02:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_listing_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='won_bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='won_listing', to='auctions.bid'),
        ),
    ]
