# Generated by Django 4.1.4 on 2023-06-20 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0013_activitybooking_is_private_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityTestimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('avatar', models.FileField(blank=True, upload_to='')),
                ('role', models.CharField(blank=True, max_length=200)),
                ('title', models.CharField(blank=True, max_length=500)),
                ('source', models.CharField(choices=[('Trip Advisor', 'Trip Advisor'), ('Trust Pilot', 'Trust Pilot'), ('Google', 'Google'), ('Others', 'Others')], default='Others', max_length=200)),
                ('review', models.TextField(blank=True)),
                ('rating', models.FloatField(default=5)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testimonials', to='activity.activity')),
            ],
        ),
    ]