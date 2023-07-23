from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.fields import related

from categories.models import Category
from users.models import CustomUser


class Position(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    bio = models.TextField()
    picture = models.ImageField(upload_to='page/picture', null=True, blank=True)
    is_organization = models.BooleanField(default=False)
    wide_picture = models.ImageField(upload_to='page/wide_picture/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    followers = models.ManyToManyField(CustomUser, related_name='followed_pages')
    followers_count = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='page_author')
    position = models.ManyToManyField(Position, related_name='page_position')

    def followers_count(self):
        return self.followers.count()

    def __str__(self):
        return self.name


class PageInteraction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_interaction')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='page_interaction')
    is_uninteresting = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'page')


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='post/picture/', null=True, blank=True)
    description = models.TextField()
    views = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=False)
    publish_date = models.DateField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField(Category, related_name='categories_post')
    author = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='page_posts')

    def comments_count(self):
        return self.comments.count()

    def __str__(self):
        return self.title


class PostLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=((1, 'Like'), (-1, 'Dislike')))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    text = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    created_at = models.DateTimeField(auto_now_add=True)


class CommentLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=((1, 'Like'), (-1, 'Dislike')))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')
