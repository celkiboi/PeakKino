# Generated by Django 4.2.13 on 2024-07-10 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0016_alter_season_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='number',
            field=models.PositiveIntegerField(),
        ),
    ]
