# Generated by Django 5.1.5 on 2025-01-31 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='weight_per_item',
            field=models.FloatField(help_text='kg'),
        ),
    ]
