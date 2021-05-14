# Generated by Django 3.2 on 2021-05-13 13:20

from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210511_0959'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favoritewatched',
            options={'ordering': ('-id',), 'verbose_name': 'Избранное/Просмотренное', 'verbose_name_plural': 'Избранные/Просмотренные'},
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to='movie', validators=[utils.validators.validate_size, utils.validators.validate_extension]),
        ),
        migrations.AlterField(
            model_name='producer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='producer', validators=[utils.validators.validate_size, utils.validators.validate_extension]),
        ),
    ]