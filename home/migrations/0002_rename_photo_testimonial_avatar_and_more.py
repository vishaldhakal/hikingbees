# Generated by Django 4.1.4 on 2023-02-04 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testimonial',
            old_name='photo',
            new_name='avatar',
        ),
        migrations.RenameField(
            model_name='testimonial',
            old_name='occupation',
            new_name='role',
        ),
    ]
