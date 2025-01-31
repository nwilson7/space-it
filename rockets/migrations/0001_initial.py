# Generated by Django 5.1.5 on 2025-01-31 12:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rocket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('cargo_capacity_kg', models.FloatField()),
                ('fuel_consumption_rate', models.FloatField(help_text='Tonnes per AU')),
                ('fuel_cost', models.FloatField(help_text='£ per tonne')),
                ('fuel_capacity', models.FloatField()),
                ('range_au', models.FloatField(editable=False)),
                ('owner', models.ForeignKey(limit_choices_to={'role': 'rocket_owner'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
