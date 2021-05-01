from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from main.models import Score, Movie


@receiver(post_save, sender=Score)
@receiver(post_delete, sender=Score)
def movie_score_update(sender, instance, **kwargs):
    movie_id = instance.movie.id
    movie = Movie.objects.get_movie(pk=movie_id).first()
    movie.avg_score = Score.objects.avg_score(pk=movie_id)
    movie.cnt_voters = Score.objects.get_cnt_voters(pk=movie_id)
    movie.save()
