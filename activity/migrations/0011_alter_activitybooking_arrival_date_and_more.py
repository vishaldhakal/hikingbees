# Generated by Django 4.1.4 on 2023-03-19 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0010_alter_activity_additional_info_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitybooking',
            name='arrival_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='activitybooking',
            name='departure_date',
            field=models.DateTimeField(null=True),
        ),
    ]
