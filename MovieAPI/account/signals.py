import os
from django.db.models.signals import post_delete, pre_delete, pre_save
from django.dispatch import receiver
from auth_.models import MainUser, Profile
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_delete, sender=Profile)
def delete_related_user(sender, instance, **kwargs):
    user = MainUser.objects.get(id=instance.user.id)
    user.delete()


@receiver(pre_delete, sender=Profile)
def delete_related_user_image(sender, instance, **kwargs):
    try:
        img = instance.__class__.objects.get(id=instance.id).image.path
        if os.path.exists(img):
            os.remove(img)
    except ObjectDoesNotExist:
        pass


@receiver(pre_save, sender=Profile)
def delete_related_user_old_image(sender, instance, **kwargs):
    try:
        old_img = instance.__class__.objects.get(id=instance.id).image.path
        try:
            new_img = instance.image.path
        except ObjectDoesNotExist:
            new_img = None
        if new_img != old_img:
            if os.path.exists(old_img):
                os.remove(old_img)
    except ObjectDoesNotExist:
        pass
