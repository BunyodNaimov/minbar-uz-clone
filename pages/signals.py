from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Page


@receiver(m2m_changed, sender=Page.followers.through)
def update_followers_count(sender, instance, **kwargs):
    instance.followers_count = instance.followers.count()
    instance.save()
