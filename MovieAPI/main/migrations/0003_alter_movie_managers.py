# Generated by Django 3.2 on 2021-04-22 17:27

from django.db import migrations
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_movie_poster'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='movie',
            managers=[
                ('objects', main.models.MovieManager()),
            ],
        ),
    ]
