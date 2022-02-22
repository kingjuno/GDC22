# Generated by Django 4.0.1 on 2022-02-17 10:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0013_emailreport_time_zone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailreport',
            name='time',
            field=models.TimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='emailreport',
            name='time_zone',
            field=models.CharField(max_length=100),
        ),
    ]