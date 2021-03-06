# Generated by Django 3.2 on 2021-05-13 16:33

from django.db import migrations, models
import utils.upload
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth_', '0003_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=utils.upload.user_avatar_directory_path, validators=[utils.validators.validate_size, utils.validators.validate_extension]),
        ),
    ]
