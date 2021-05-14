import os

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver
from main.models import Score, Movie, Producer


@receiver(post_save, sender=Score)
@receiver(post_delete, sender=Score)
def movie_score_update(sender, instance, **kwargs):
    movie_id = instance.movie.id
    movie = Movie.objects.get_movie(pk=movie_id).first()
    movie.avg_score = Score.objects.avg_score(pk=movie_id)
    movie.cnt_voters = Score.objects.get_cnt_voters(pk=movie_id)
    movie.save()


@receiver(pre_delete, sender=Movie)
def delete_movie_poster(sender, instance, **kwargs):
    try:
        img = instance.__class__.objects.get(id=instance.id).poster or None
        if img and os.path.exists(img.path):
            os.remove(img.path)
    except ObjectDoesNotExist:
        pass


@receiver(pre_save, sender=Movie)
def delete_movie_old_poster(sender, instance, **kwargs):
    try:
        old_img = instance.__class__.objects.get(id=instance.id).poster or None
        new_img = instance.poster or None
        if old_img and new_img != old_img:
            if os.path.exists(old_img.path):
                os.remove(old_img.path)
    except ObjectDoesNotExist:
        pass


@receiver(pre_delete, sender=Producer)
def delete_producer_image(sender, instance, **kwargs):
    try:
        img = instance.__class__.objects.get(id=instance.id).image or None
        if img and os.path.exists(img.path):
            os.remove(img.path)
    except ObjectDoesNotExist:
        pass


@receiver(pre_save, sender=Producer)
def delete_producer_old_image(sender, instance, **kwargs):
    try:
        old_img = instance.__class__.objects.get(id=instance.id).image or None
        new_img = instance.image or None
        if old_img and new_img != old_img:
            if os.path.exists(old_img.path):
                os.remove(old_img.path)
    except ObjectDoesNotExist:
        pass
