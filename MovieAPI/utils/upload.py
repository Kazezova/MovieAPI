def user_avatar_directory_path(instance, filename):
    user = instance.user
    return f'user/{user.id}_{filename}'


def producer_image_directory_path(instance, filename):
    producer = instance
    return f'producer/{producer.id}_{filename}'


def movie_image_directory_path(instance, filename):
    movie = instance
    return f'movie/{movie.id}_{filename}'
