# Generated by Django 5.1.5 on 2025-01-31 16:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('destination', '0001_initial'),
        ('rockets', '0003_alter_rocket_fuel_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Launch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('launch_date', models.DateField()),
                ('remaining_capacity_kg', models.FloatField()),
                ('launch_cost', models.FloatField()),
                ('price_per_kg', models.FloatField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='destination.destination')),
                ('rocket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rockets.rocket')),
            ],
        ),
    ]
