# Generated by Django 4.2.11 on 2024-04-15 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_movie_resource_series_remove_video_age_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.resource'),
        ),
    ]
