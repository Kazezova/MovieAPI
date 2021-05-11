from django.db.models.signals import post_delete
from django.dispatch import receiver
from auth_.models import MainUser, Profile


@receiver(post_delete, sender=Profile)
def delete_related_user(sender, instance, **kwargs):
    user = MainUser.objects.get(id=instance.user.id)
    user.delete()
