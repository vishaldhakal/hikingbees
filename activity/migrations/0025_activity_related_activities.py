# Generated by Django 5.1.6 on 2025-03-28 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0024_alter_videoreview_subtitle_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='related_activities',
            field=models.ManyToManyField(blank=True, to='activity.activity'),
        ),
    ]
