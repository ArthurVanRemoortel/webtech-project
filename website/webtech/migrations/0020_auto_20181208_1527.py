# Generated by Django 2.1.3 on 2018-12-08 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webtech', '0019_auto_20181208_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]