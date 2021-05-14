import os
from django.core.exceptions import ValidationError

MAX_FILE_SIZE = 3145728
ALLOWED_EXTENSIONS = ['.jpg', '.png']


def validate_size(value):
    if value.size > MAX_FILE_SIZE:
        raise ValidationError(f'Max file size is: {MAX_FILE_SIZE}')


def validate_extension(value):
    split_ext = os.path.splitext(value.name)

    if len(split_ext) > 1:
        ext = split_ext[1]
        if ext.lower() not in ALLOWED_EXTENSIONS:
            raise ValidationError(f'Not allowed file extension, valid extensions: {ALLOWED_EXTENSIONS}')
