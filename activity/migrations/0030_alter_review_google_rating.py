# Generated by Django 5.1.6 on 2025-04-23 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0029_review_google_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='google_rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
