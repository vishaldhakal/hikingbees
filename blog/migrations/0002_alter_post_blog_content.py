# Generated by Django 4.1.4 on 2023-03-08 02:20

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
    ]
