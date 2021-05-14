from django.db import models
from django.db.models import Avg, Func


class Round(Func):
    function = "ROUND"
    template = "%(function)s(%(expressions)s::numeric, 1)"


class MovieManager(models.Manager):

    def get_movie(self, pk):
        return self.filter(pk=pk)


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
        return self.filter(movie__id=movie_id)

    def get_user_movie_review(self, user_id, movie_id):
        return self.filter(author__id=user_id, movie__id=movie_id)

    def get_review(self, review_id):
        return self.filter(id=review_id)


class FavoriteWatchedManager(models.Manager):

    def get_relation(self, user_id, movie_id):
        return self.filter(user__id=user_id, movie__id=movie_id)

    def get_favorite_list(self, user_id):
        return self.filter(user__id=user_id, favorite=True)

    def get_favorite(self, user_id, movie_id):
        return self.filter(user__id=user_id, movie__id=movie_id, favorite=True)

    def get_watched_list(self, user_id):
        return self.filter(user__id=user_id, watched=True)

    def get_watched(self, user_id, movie_id):
        return self.filter(user__id=user_id, movie__id=movie_id, watched=True)
