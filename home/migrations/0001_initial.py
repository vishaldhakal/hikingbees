# Generated by Django 4.1.4 on 2023-01-20 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HeroSectionContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero_section_title', models.CharField(default='Welcome to Hiking Bees : Your Ultimate Guide to Exploring the Great Outdoors', max_length=328)),
                ('hero_section_subtitle', models.CharField(default='Discover The Best Hiking Trails And Bee-Watching Spots On Your Next Adventure. Book A Trip Now', max_length=328)),
                ('hero_section_image', models.ImageField(blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('role', models.CharField(blank=True, max_length=200)),
                ('photo', models.ImageField(blank=True, upload_to='')),
                ('facebook', models.URLField(blank=True)),
                ('instagram', models.URLField(blank=True)),
                ('linkedin', models.URLField(blank=True)),
                ('twitter', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('photo', models.ImageField(blank=True, upload_to='')),
                ('occupation', models.CharField(blank=True, max_length=200)),
                ('review', models.TextField(blank=True)),
                ('rating', models.FloatField(default=5)),
            ],
        ),
    ]
