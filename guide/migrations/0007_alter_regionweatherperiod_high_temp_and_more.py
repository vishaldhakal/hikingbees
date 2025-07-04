# Generated by Django 5.1.6 on 2025-06-30 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0006_alter_regionweatherperiod_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regionweatherperiod',
            name='high_temp',
            field=models.IntegerField(blank=True, help_text='High temperature (°C)', null=True),
        ),
        migrations.AlterField(
            model_name='regionweatherperiod',
            name='low_temp',
            field=models.IntegerField(blank=True, help_text='Low temperature (°C)', null=True),
        ),
    ]
