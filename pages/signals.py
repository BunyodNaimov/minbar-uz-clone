from django.db.models import Count
from django.db.models.signals import m2m_changed, post_save, post_delete
from django.dispatch import receiver
from .models import Page, Comment, Post


@receiver(m2m_changed, sender=Page.followers.through)
def update_followers_count(sender, instance, **kwargs):
    instance.followers_count = instance.followers.count()
    instance.save()


@receiver(post_save, sender=Post)
@receiver(post_delete, sender=Post)
def update_comments_count(sender, instance, **kwargs):
    post = instance.post
    post.comments_count = post.comments.aggregate(Count('id'))['id__count']
    post.save()
