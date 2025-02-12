# Generated by Django 5.1.5 on 2025-01-31 14:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('destination', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargoname', models.CharField(max_length=255)),
                ('weight_per_item', models.FloatField()),
                ('number_of_items', models.PositiveIntegerField()),
                ('launched', models.BooleanField(default=False)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='destination.destination')),
                ('owner', models.ForeignKey(limit_choices_to={'role': 'cargo_owner'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
