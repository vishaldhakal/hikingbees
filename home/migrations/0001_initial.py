# Generated by Django 4.1.4 on 2023-02-10 15:56

from django.db import migrations, models
import django.db.models.deletion
import django_summernote.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('link_to_website', models.URLField(blank=True)),
                ('image', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='FAQCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='InnerDropdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activites', models.ManyToManyField(blank=True, to='activity.activity')),
                ('activity_region', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='activity.activityregion')),
            ],
        ),
        migrations.CreateModel(
            name='Partners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('link_to_website', models.URLField(blank=True)),
                ('image', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero_title_line1', models.CharField(default='Line 1', max_length=328)),
                ('hero_title_line2', models.CharField(default='Line 2', max_length=328)),
                ('hero_title_line3', models.CharField(default='Line 3', max_length=328)),
                ('hero_section_subtitle', models.TextField(default='Discover The Best Hiking Trails And Bee-Watching Spots On Your Next Adventure. Book A Trip Now')),
                ('hero_section_image', models.FileField(blank=True, upload_to='')),
            ],
            options={
                'verbose_name': 'Site Configuration',
            },
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('role', models.CharField(blank=True, max_length=200)),
                ('photo', models.FileField(blank=True, upload_to='')),
                ('about', django_summernote.fields.SummernoteTextField(blank=True)),
                ('type', models.CharField(choices=[('Executive Team', 'Executive Team'), ('Representative', 'Representative'), ('Trekking Guides', 'Trekking Guides'), ('Tour Guide', 'Tour Guide')], default='Representative', max_length=300)),
                ('email', models.CharField(max_length=200)),
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
                ('avatar', models.FileField(blank=True, upload_to='')),
                ('role', models.CharField(blank=True, max_length=200)),
                ('review', models.TextField(blank=True)),
                ('rating', models.FloatField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='TreekingNavDropdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('innerdropdowns', models.ManyToManyField(blank=True, to='home.innerdropdown')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OtherActivitiesNavDropdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_categories', models.ManyToManyField(blank=True, to='activity.activitycategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=500)),
                ('answer', models.TextField(max_length=1000)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.faqcategory')),
            ],
        ),
        migrations.CreateModel(
            name='DestinationNavDropdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destinations', models.ManyToManyField(blank=True, to='activity.destination')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClimbingNavDropdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('innerdropdowns', models.ManyToManyField(blank=True, to='home.innerdropdown')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]