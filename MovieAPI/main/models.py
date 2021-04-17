from django.db import models
from utils.constants import COUNTRIES, GENDERS
from auth_.models import MainUser
from django.utils import timezone


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Producer(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
    country = models.CharField(max_length=2, choices=COUNTRIES, verbose_name='Страна')
    place_of_birth = models.CharField(verbose_name='Место рождения', max_length=100, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.IntegerField(choices=GENDERS)
    image = models.ImageField(null=True, blank=True)
    genre = models.ManyToManyField(Genre)
    total_movies = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Режиссер'
        verbose_name_plural = 'Режиссеры'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class MPAA(models.Model):
    title = models.CharField(max_length=100)
    meaning = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтингы'

    def __str__(self):
        return self.title


class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    original_title = models.CharField(max_length=255, verbose_name='Оригинальное название')
    poster = models.ImageField(null=True, blank=True)
    tagline = models.TextField(verbose_name='Слоган', null=True, blank=True)
    short_description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание', null=True, blank=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанры')
    release_date = models.DateField(verbose_name='Год производства')
    country = models.CharField(max_length=2, choices=COUNTRIES, verbose_name='Страна')
    producer = models.ForeignKey(Producer, on_delete=models.SET_NULL, verbose_name='Режиссер', null=True)
    budget = models.IntegerField(verbose_name='Бюджет', null=True, blank=True)
    revenue = models.IntegerField(verbose_name='Выручка', null=True, blank=True)
    rating = models.ForeignKey(MPAA, on_delete=models.SET_NULL, verbose_name='Ограничение', null=True)
    time = models.IntegerField(verbose_name='Продолжительность в минутах')
    avg_score = models.DecimalField(max_digits=1, decimal_places=1, verbose_name='Средняя оценка', null=True,
                                    blank=True)
    cnt_voters = models.IntegerField(verbose_name='Количество проголосовавших', default=0)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.original_title


class UniqueUserMovie(models.Model):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        unique_together = ('user', 'movie')


class Score(UniqueUserMovie):
    score = models.IntegerField(choices=list(zip(range(1, 11), range(1, 11))))

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


class Favorite(UniqueUserMovie):
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Watched(UniqueUserMovie):
    class Meta:
        verbose_name = 'Просмотренное'
        verbose_name_plural = 'Просмотренные'


class Review(models.Model):
    author = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)
    content = models.TextField()

    class Meta:
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'
        ordering = ('-created_date',)
