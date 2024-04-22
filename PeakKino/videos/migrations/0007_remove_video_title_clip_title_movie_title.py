# Generated by Django 4.2.11 on 2024-04-15 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_clip_season_show_remove_episode_path_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='title',
        ),
        migrations.AddField(
            model_name='clip',
            name='title',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='title',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]