# Generated by Django 2.1.3 on 2018-12-15 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webtech', '0002_delete_venuereview'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venuereview',
            name='venue',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='webtech.Venue'),
        ),
    ]
