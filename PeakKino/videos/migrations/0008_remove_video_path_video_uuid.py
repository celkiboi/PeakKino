# Generated by Django 4.2.11 on 2024-04-15 22:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0007_remove_video_title_clip_title_movie_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='path',
        ),
        migrations.AddField(
            model_name='video',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True),
        ),
    ]
