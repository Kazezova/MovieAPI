from django.db import models
from django.db.models import Avg, Func


class MovieManager(models.Manager):

    def get_movie(self, pk):
        return self.filter(pk=pk)


class Round(Func):
    function = "ROUND"
    template = "%(function)s(%(expressions)s::numeric, 1)"


class ScoreManager(models.Manager):

    def get_movie_scores(self, movie_id):
        return self.filter(movie__id=movie_id)

    def get_movie_score_by_user(self, user_id, movie_id):
        return self.filter(user__id=user_id, movie__id=movie_id)

    def get_cnt_voters(self, pk):
        return self.get_movie_scores(pk).count()

    def avg_score(self, pk):
        return self.get_movie_scores(pk).aggregate(rounded_avg_score=Round(Avg('score')))['rounded_avg_score']


class ReviewManager(models.Manager):

    def get_movie_reviews(self, movie_id):
        return self.filter(movie__pk=movie_id)

    def get_user_movie_review(self, user_id, movie_id):
        return self.filter(user__id=user_id, movie__pk=movie_id)
