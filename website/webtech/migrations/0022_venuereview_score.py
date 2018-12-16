# Generated by Django 2.1.3 on 2018-12-15 11:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webtech', '0021_auto_20181209_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='venuereview',
            name='score',
            field=models.IntegerField(default=10, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
    ]