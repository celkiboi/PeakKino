# Generated by Django 4.2.11 on 2024-04-15 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='age_rating',
            field=models.CharField(choices=[('18', '18+'), ('15', '15+'), ('12', '12+'), ('7', '7+')], default=18, max_length=3),
            preserve_default=False,
        ),
    ]
