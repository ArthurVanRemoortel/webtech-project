# Generated by Django 2.1.3 on 2018-12-16 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webtech', '0029_merge_20181216_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(upload_to='images/uploaded'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
