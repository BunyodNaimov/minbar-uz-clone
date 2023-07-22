from rest_framework import serializers

from categories.models import Category
from categories.serializers import CategorySerializer
from pages.models import Page, Post, PageInteraction, Position, PostLike
from users.models import CustomUser


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'id', 'name', 'slug', 'picture', 'author', 'is_organization', 'followers_count', 'followed'
        )
        read_only_fields = ('id', 'picture', 'followers_count', 'followed')


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'name')
        read_only_fields = ('id',)


class PostAuthorSerializer(serializers.ModelSerializer):
    position = PositionSerializer(read_only=True, many=True)

    class Meta:
        model = Page
        fields = ('id', 'name', 'position')
        read_only_fields = ('id',)


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('id', 'post', 'value')


class PostSerializer(serializers.ModelSerializer):
    author = PostAuthorSerializer(read_only=True)
    categories = CategorySerializer(read_only=True, many=True)
    likes = serializers.IntegerField(read_only=True)
    dislikes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'slug', 'image', 'description', 'views', 'visible', 'allow_comments', 'publish_date',
            'likes', 'dislikes', 'categories', 'author')
        read_only_fields = ('id',)


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'description', 'image', 'author', 'views', 'visible')
        read_only_fields = ('id',)


class BlockedPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageInteraction
        fields = ('id', 'user', 'page')
        read_only_fields = ('id',)
