from django.db import models

from users.models import CustomUser


# class Page(models.Model):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField(max_length=255)
#     bio = models.TextField()
#     picture = models.ImageField(upload_to='page/picture')
#     is_organization = models.BooleanField(default=False)
#     wide_picture = models.ImageField(upload_to='page/wide_picture/', null=True, blank=True)
#     author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='page_author')
#     created_at = models.DateTimeField(auto_now=True)
#     updated_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='post/picture/', null=True, blank=True)
    description = models.TextField()
    views = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=False)
    publish_date = models.DateField
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='post_author')
