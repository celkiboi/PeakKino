# Generated by Django 4.2.13 on 2024-07-07 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0012_subtitle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subtitle',
            name='file_extension',
        ),
    ]
