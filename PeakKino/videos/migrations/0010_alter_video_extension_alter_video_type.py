# Generated by Django 4.2.11 on 2024-04-15 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0009_video_extension'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='extension',
            field=models.CharField(default='mp4', max_length=8),
        ),
        migrations.AlterField(
            model_name='video',
            name='type',
            field=models.CharField(choices=[('movie', 'Movie'), ('episode', 'Episode'), ('clip', 'Clip'), ('other', 'Other')], max_length=10),
        ),
    ]
