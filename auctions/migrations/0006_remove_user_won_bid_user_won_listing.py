# Generated by Django 5.0.1 on 2024-01-18 03:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_remove_listing_won_bid_user_won_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='won_bid',
        ),
        migrations.AddField(
            model_name='user',
            name='won_listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='auctions.listing'),
        ),
    ]
